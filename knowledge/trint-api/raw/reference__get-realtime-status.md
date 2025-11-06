---
source: https://dev.trint.com/reference/get-realtime-status
retrieved: 2025-11-06T03:44:37.793354+00:00
---

# Get realtime status
get https://api.trint.com/transcripts/realtime/{trint-id}
Get the current status of a realtime
  * status: **possible statuses** : "STARTING" | "TRANSCRIBING" | "STOPPING" | "STOPPED" | "FAILED" | "UNKNOWN"
  * warnings: array of strings containing warnings during stream lifetime
  * errors: array of strings containing errors during stream lifetime
  * started: UTC date/time realtime started
  * expires: UTC date/time realtime expires (6 hours after it starts)
