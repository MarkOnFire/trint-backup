#!/usr/bin/env python3.11
"""Scrape the Trint API documentation into knowledge/trint-api/raw."""

from __future__ import annotations

import asyncio
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit, urlunsplit

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.async_configs import BrowserConfig
from crawl4ai.async_crawler_strategy import AsyncHTTPCrawlerStrategy
from crawl4ai.async_logger import LogLevel
from crawl4ai.cache_context import CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, FilterChain, URLPatternFilter

BASE_URL = "https://dev.trint.com"
ALLOWED_PATH_PREFIXES: tuple[str, ...] = ("/", "/docs", "/reference")
EXCLUDED_PATH_PREFIXES: tuple[str, ...] = ("/login",)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_ROOT = PROJECT_ROOT / "knowledge" / "trint-api"
TARGET_DIR = KNOWLEDGE_ROOT / "raw"
MANIFEST_PATH = KNOWLEDGE_ROOT / "manifest.json"


def canonicalize_url(url: str) -> str:
    """Normalize the URL so duplicates collapse."""
    parts = urlsplit(url)
    scheme = parts.scheme or "https"
    netloc = parts.netloc or urlsplit(BASE_URL).netloc
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    # Sort query params for stability
    query = "&".join(
        sorted(filter(None, parts.query.split("&")))
    )
    return urlunsplit((scheme, netloc, path or "/", query, ""))


def should_keep(url: str) -> bool:
    """Filter crawled URLs down to the published documentation pages."""
    parts = urlsplit(url)
    if parts.netloc and parts.netloc != urlsplit(BASE_URL).netloc:
        return False

    path = parts.path or "/"
    if any(path.startswith(prefix) for prefix in EXCLUDED_PATH_PREFIXES):
        return False

    return any(path.startswith(prefix) for prefix in ALLOWED_PATH_PREFIXES)


def slugify_url(url: str) -> str:
    """Turn a URL into a filesystem-safe slug."""
    parts = urlsplit(url)
    segments = [segment for segment in parts.path.strip("/").split("/") if segment]
    if not segments:
        segments = ["index"]

    slug = "__".join(segments)
    if parts.query:
        query_part = re.sub(r"[^a-zA-Z0-9]+", "-", parts.query)
        slug = f"{slug}__{query_part}"

    slug = re.sub(r"[^a-z0-9_-]+", "-", slug.lower()).strip("-")
    return slug or "index"


def extract_title(markdown: str) -> str:
    """Grab the first H1 from the markdown payload."""
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return ""


async def crawl_docs() -> Iterable:
    """Run the Crawl4AI deep crawl across the docs site."""
    os.environ.setdefault("CRAWL4_AI_BASE_DIRECTORY", str(PROJECT_ROOT))

    filter_chain = FilterChain([URLPatternFilter(f"{BASE_URL}/*")])
    strategy = BFSDeepCrawlStrategy(
        max_depth=5,
        filter_chain=filter_chain,
        include_external=False,
        max_pages=250,
    )

    crawl_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        deep_crawl_strategy=strategy,
        check_robots_txt=False,
        target_elements=["article.rm-Article"],
        word_count_threshold=1,
    )

    crawler = AsyncWebCrawler(
        crawler_strategy=AsyncHTTPCrawlerStrategy(),
        config=BrowserConfig(verbose=False),
        base_directory=str(PROJECT_ROOT),
    )
    crawler.logger.verbose = False
    crawler.logger.log_level = LogLevel.FATAL

    async with crawler:
        container = await crawler.arun(f"{BASE_URL}/", crawl_config)

    return list(container)


def write_documents(results: Iterable) -> dict:
    """Persist scraped markdown documents and return the manifest."""
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # Clean out previous markdown artifacts so stale pages do not linger.
    for md_file in TARGET_DIR.glob("*.md"):
        md_file.unlink()

    retrieved_at = datetime.now(timezone.utc).isoformat()
    manifest: list[dict] = []
    seen_urls: set[str] = set()

    for result in results:
        url = canonicalize_url(result.redirected_url or result.url)
        if url in seen_urls:
            continue
        seen_urls.add(url)

        if not result.success or not should_keep(url):
            continue

        markdown = str(result.markdown or "").strip()
        if not markdown:
            continue

        slug = slugify_url(url)
        output_path = TARGET_DIR / f"{slug}.md"

        title = extract_title(markdown) or slug.replace("_", " ").title()
        front_matter = (
            f"---\n"
            f"source: {url}\n"
            f"retrieved: {retrieved_at}\n"
            f"---\n\n"
        )

        output_path.write_text(front_matter + markdown + "\n", encoding="utf-8")

        manifest.append(
            {
                "title": title,
                "url": url,
                "slug": slug,
                "path": f"knowledge/trint-api/raw/{output_path.name}",
                "retrieved": retrieved_at,
                "status_code": result.status_code or 200,
            }
        )

    manifest.sort(key=lambda item: item["url"])

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {
        "retrieved": retrieved_at,
        "count": len(manifest),
        "manifest": manifest,
    }


def main() -> None:
    results = asyncio.run(crawl_docs())
    summary = write_documents(results)
    print(
        f"Wrote {summary['count']} Trint documentation pages to "
        f"{TARGET_DIR.relative_to(PROJECT_ROOT)}"
    )


if __name__ == "__main__":
    main()
