---
source: https://dev.trint.com/reference/jsontrint-id
retrieved: 2025-11-06T03:44:37.793354+00:00
---

# JSON
get https://api.trint.com/export/json/{trint-id}
Export a Trint in JSON format
## 
Realtime Statuses:
[](https://dev.trint.com/reference/jsontrint-id#realtime-statuses)
  * "STARTING" | "TRANSCRIBING" | "STOPPING" | "STOPPED" | "FAILED"
  * If the Trint being exported is not a realtime stream then the field will be null
