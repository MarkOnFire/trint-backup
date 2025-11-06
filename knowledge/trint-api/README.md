# Trint API Knowledge Base

This folder contains a point-in-time scrape of every published page under <https://dev.trint.com>, covering the Trint API guides and reference material. Content is stored as markdown with per-page provenance in `raw/`, and a machine-readable inventory lives in `manifest.json`.

- **Pages captured:** 68
- **Source:** https://dev.trint.com
- **Last scrape:** 2025-11-06T03:44:37.793354+00:00 (UTC)
- **Scraper:** `python3.11 scripts/scrape_trint_docs.py`

## Refresh Process
1. Ensure Python 3.11+ and Crawl4AI dependencies are available (`python3.11 -m pip install crawl4ai`).
2. From the repository root, run `python3.11 scripts/scrape_trint_docs.py`. The script clears `knowledge/trint-api/raw`, re-crawls the docs with Crawl4AI (HTTP strategy + BFS deep crawl), and rewrites `manifest.json`.
3. Review `git status` and `git diff knowledge/trint-api` to verify expected changes (page additions, removals, or content shifts).
4. Commit the refreshed artifacts with a message such as `Update Trint API knowledge base` and push to the shared remote.

## Update Strategy
- **Cadence:** Re-scrape at least once per month and whenever Trint announces API changes or before running archival workflows.
- **Responsible party:** Repository owner (Mark R.) or a delegated engineer on the archival project.
- **Tooling:** `scripts/scrape_trint_docs.py` for collection, git history to audit diffs, and `manifest.json` to track timestamps.
- **Change monitoring:** Compare successive manifests or run `rg` across `knowledge/trint-api/raw` to spot breaking changes (e.g., parameter renames). Log noteworthy API deltas in the project README or task tracker so downstream scripts can be updated promptly.

