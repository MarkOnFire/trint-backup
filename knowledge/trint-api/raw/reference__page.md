---
source: https://dev.trint.com/reference/page
retrieved: 2025-11-06T03:44:37.793354+00:00
---

# List Files
get https://api.trint.com/transcripts/
The list files endpoint returns a list of files (id, title etc) belonging to the current user or accessible via a specified Shared Drive. If a sharedDriveId, the results will list the contents of that drive (or drive Folder if a folderId is also supplied), no matter which user the Trints belong to. Otherwise the results will list the Trints belonging to the user whose API key is supplied. NB: Workspace is simply the old terminology for Shared Drive, calls can be made with a workspaceId instead of a sharedDriveId for backwards compatibility.
