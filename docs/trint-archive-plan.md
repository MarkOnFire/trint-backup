# Trint Transcript Archive Plan

## Objective
- Build a one-off ingestion script that exports every transcript in the client's Trint account to both Markdown and Microsoft Word while preserving folder/workspace context and relevant metadata.

## Authentication & Environment
- API requests use HTTP Basic Auth with the API key ID and secret, per the official guidance. Document legacy single-token auth only as a fallback for older keys. (knowledge/trint-api/raw/docs__trint-api-keys.md:1)
- Determine whether the account resides on the US or EU tenant before making calls; switch all API and upload base URLs accordingly. (knowledge/trint-api/raw/docs__us-vs-eu-tenant.md:1)

## Core Resources & Endpoints
| Purpose | Method & URL | Notes |
| --- | --- | --- |
| Enumerate shared drives/workspaces | `GET https://api.trint.com/workspaces/` | Capture name → `sharedDriveId` map to scope transcript queries. (knowledge/trint-api/raw/reference__list-workspaces.md:1) |
| Enumerate folders inside a shared drive | `GET https://api.trint.com/folders/` | Filter by `sharedDriveId` and/or `parentId` to mirror the UI hierarchy. (knowledge/trint-api/raw/reference__folders.md:1) |
| List transcripts | `GET https://api.trint.com/transcripts/?limit=100&skip=0&sharedDriveId=...&folderId=...` | Paginate until exhausted; default limit is 100. (knowledge/trint-api/raw/reference__page.md:1) |
| Fetch transcript metadata/file bundle | `GET https://api.trint.com/transcripts/file/{id}` | Returns the ZIP that the editor downloads; useful for validating timestamps and speaker labels. (knowledge/trint-api/raw/reference__get-file.md:1) |
| Export transcript as DOCX | `GET https://api.trint.com/export/docx/{trint-id}` | Primary source for the Word deliverable. (knowledge/trint-api/raw/reference__transcript-docx.md:1) |
| Export transcript as HTML | `GET https://api.trint.com/export/html/{trint-id}` | Feed HTML into Markdown conversion to retain speaker structure. (knowledge/trint-api/raw/reference__html.md:1) |
| Export transcript as JSON (optional) | `GET https://api.trint.com/export/json/{trint-id}` | Rich structure for advanced post-processing (timestamps, markers). (knowledge/trint-api/raw/reference__jsontrint-id.md:1) |
| Export transcript as plain text (optional) | `GET https://api.trint.com/export/text/{trint-id}` | Fallback if HTML-to-Markdown proves noisy. (knowledge/trint-api/raw/reference__text.md:1) |

> Translate the base URL to `https://api.eu.trint.com/` and `https://upload.eu.trint.com/` when targeting the EU tenant.

## Data Flow
1. **Configuration**  
   - Accept CLI flags/env vars for API key, tenant (`us`/`eu`), output root, rate limit, and optional workspace/folder filters.
   - Derive base URLs from tenant selection. (knowledge/trint-api/raw/docs__us-vs-eu-tenant.md:1)
2. **Workspace & Folder Discovery**  
   - Call `GET /workspaces/` to enumerate shared drives.  
   - For each workspace, call `GET /folders/` to collect folder IDs and parent chains.
3. **Transcript Enumeration**  
   - Page through `GET /transcripts/` for each workspace/folder combination.  
   - Cache transcript metadata (titles, owners, created/updated timestamps, duration) for later manifesting.
4. **Asset Export per Transcript**  
   - Request DOCX export and persist to `.../word/{trint-id}.docx`. (knowledge/trint-api/raw/reference__transcript-docx.md:1)  
   - Request HTML export, convert to Markdown (e.g., Python `markdownify`/`pandoc`) and store in `.../markdown/{trint-id}.md`. (knowledge/trint-api/raw/reference__html.md:1)  
   - Optionally store JSON export for auditing or richer Markdown templating. (knowledge/trint-api/raw/reference__jsontrint-id.md:1)
5. **Manifesting**  
   - Produce a JSON or CSV manifest capturing transcript ID, title, workspace, folder path, creation/update timestamps, language, and the relative paths of generated assets.
6. **Verification**  
   - Sample a subset of DOCX/Markdown outputs for fidelity (speaker segmentation, timestamps, captions).  
   - Compare transcript counts against the API `totalCount` for each workspace to confirm completeness.

## Storage Layout
```
archive_root/
  manifests/
    trint-archive-YYYYMMDD.json
  transcripts/
    {workspaceSlug}/
      {folderPath}/
        {trintId}/
          metadata.json
          transcript.md
          transcript.docx
          raw/
            transcript.html
            transcript.json
```

## Operational Considerations
- **Pagination:** Track `skip` offsets and accumulate until the API returns fewer than the requested `limit`. (knowledge/trint-api/raw/docs__trint-api-keys.md:1)
- **Rate limiting:** Trint does not publish explicit limits; add a modest backoff (e.g., 5 req/sec) and retry with exponential jitter on HTTP 429/5xx.
- **Large accounts:** Allow resume support by persisting progress markers (last processed transcript ID per workspace).  
- **Error handling:** Capture non-200 responses with context and continue; log unresolved transcripts for manual follow-up.  
- **EU data residency:** If the account is on the EU tenant, ensure exports are saved on EU-controlled storage if required by the client’s compliance policy. (knowledge/trint-api/raw/docs__us-vs-eu-tenant.md:1)
- **Optional assets:** Consider downloading caption formats (SRT/WebVTT) and CSVs if the client may need them later. (knowledge/trint-api/raw/reference__webvtttrint-id.md:1)

## Open Questions
- `GET /transcripts/file/{id}` response structure is undocumented in this scrape; validate whether it contains additional metadata worth archiving. (knowledge/trint-api/raw/reference__get-file.md:1)
- Confirm whether DOCX export includes speaker labels and timestamps; if not, combine JSON export plus custom templating to generate Markdown. (knowledge/trint-api/raw/reference__transcript-docx.md:1, knowledge/trint-api/raw/reference__jsontrint-id.md:1)
- Determine whether the account uses Story files or translations that also need preservation. (knowledge/trint-api/raw/reference__story-files.md:1, knowledge/trint-api/raw/reference__get-translations.md:1)

## Next Implementation Steps
1. Prototype a small Python client that authenticates, lists transcripts, and downloads one transcript’s DOCX/HTML/JSON bundle.  
2. Finalize Markdown conversion pipeline and define metadata schema for manifests.  
3. Add retry/backoff utilities and optional concurrency controls.  
4. Dry-run against a sandbox or limited workspace before running the full archive.

