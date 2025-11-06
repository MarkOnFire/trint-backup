---
source: https://dev.trint.com/reference/events
retrieved: 2025-11-06T03:44:37.793354+00:00
---

# Webhook Event Types
Events that can be dispatched by Trint to your own endpoint.
## 
TRANSCRIPT_COMPLETE
[](https://dev.trint.com/reference/events#transcript_complete)
Dispatched when an upload file finishes transcribing.
Payload
```
{ 
  eventType: 'TRANSCRIPT_COMPLETE',
  transcriptId: '<TRINT_ID>',
  title: 'myFile.mp4',
  user: '[email protected][](https://dev.trint.com/cdn-cgi/l/email-protection)',
  metadata: 'some opaque metadata string' 
}
```

Key name | Type | Description  
---|---|---  
eventType | String | Event type of the callback  
transcriptId | String | The ID of the Trint that has completed transcribing  
title | String | Title of the Trint  
user | String | Username of the user attached to the Trint  
metadata | String | If metadata was supplied at the time of upload then it will be reflected back here.  
## 
TRANSCRIPT_VERIFIED
[](https://dev.trint.com/reference/events#transcript_verified)
Dispatched when a transcript has been fully verified in the editor. Also applies to transcripts which are shared with you.
Payload
```
{ 
  eventType: 'TRANSCRIPT_VERIFIED',
  transcriptId: '<TRINT_ID>',
  title: 'myFile.mp4',
  user: '[email protected][](https://dev.trint.com/cdn-cgi/l/email-protection)',
  metadata: 'some opaque metadata string' 
}
```

Key name | Type | Description  
---|---|---  
eventType | String | Event type of the callback  
transcriptId | String | The ID of the Trint that has been fully verified  
title | String | Title of the Trint  
user | String | Username of the user attached to the Trint  
metadata | String | If metadata was supplied at the time of upload then it will be reflected back here.  
## 
TRANSCRIPT_NEW_VERSION (BETA)
[](https://dev.trint.com/reference/events#transcript_new_version-beta)
Dispatched when there is a new transcript version. Also applies to transcripts which are shared with you. Available from 10 Feb 2025.
Payload
```
{ 
  eventType: 'TRANSCRIPT_NEW_VERSION',
  transcriptId: '<TRINT_ID>',
  title: 'myFile.mp4',
  user: '[email protected][](https://dev.trint.com/cdn-cgi/l/email-protection)'
}
```

Key name | Type | Description  
---|---|---  
eventType | String | Event type of the callback  
transcriptId | String | The ID of the Trint that has been fully verified  
title | String | Title of the Trint  
user | String | Username of the user attached to the Trint
