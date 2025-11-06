---
source: https://dev.trint.com/docs/trint-api-keys
retrieved: 2025-11-06T03:44:37.793354+00:00
---

# Trint API Keys and Authentication
## Trint API Keys
As of October 2024, Trint is now using Basic Authentication for our API calls. Trint users can generate and revoke API keys on the [API](https://app.trint.com/account/api) page of our webapp.
Users can create up 25 USER keys, and up to 25 ORGANIZATION keys which can be shared across the whole account. USER keys will be disabled if a user closes down their individual Trint account, while ORGANIZATION keys remain as long as the organisation retains their Trint account. This enables the use of specific keys for specific integrations and simple roll-over of keys whenever required.
_Please note - when using an ORGANIZATION key your API calls will assume the identity of the account owner when it comes to Shared Drive membership and the list of visible Trints, and not the identity of the user who created the key. This means that if you need to access a Shared Drive while using an ORGANIZATION key, you must ensure that the user registered as the account owner is a member of that Shared Drive._
Trint API keys come in two parts, a Key ID (which remains visible after the key is created) and a Key Secret (which is only shown to the user at the time of creation). Once a Key has been created we will never show the Secret again or allow the value to be changed, so users must make a record at the time of creation. Replacement keys can be created and revoked as necessary to rotate credentials at the time of your choosing. Keys can be created with an expiry date (after which time they stop working) or set to never expire.
## Basic Authentication
Each API call is authenticated using Basic Authentication (see [here](https://datatracker.ietf.org/doc/html/rfc7617)) with the API Key ID acting as the `user-id` and the API Key Secret acting as the `password`. This means that a header ('Authorization') must be sent with each request, set to the Base64 encoded value of the Key Id and Secret combined (separated by a colon). For example: 
#### Key / Secret Value:
Example Key Id: `AK-12345ABCDE`  
Example Key Secret: `this15SECRET_CXJK3ctglt6LOpYxRmZ`
Combined credentials: `AK-12345ABCDE:this15SECRET_CXJK3ctglt6LOpYxRmZ`  
Base64 encoded: `QUstMTIzNDVBQkNERTp0aGlzMTVTRUNSRVRfQ1hKSzNjdGdsdDZMT3BZeFJtWg==`
```
Authorization: Basic QUstMTIzNDVBQkNERTp0aGlzMTVTRUNSRVRfQ1hKSzNjdGdsdDZMT3BZeFJtWg==
```

In practice you will not need to perform this step manually, as most languages, tools, or other systems will take care of it for you.
#### Example call using API Keys:
CurlJavascriptPython
```
curl --request GET \
     -u "AK-12345ABCDE:this15SECRET_CXJK3ctglt6LOpYxRmZ"
     --url 'https://api.trint.com/transcripts/?limit=100&skip=0' \
     --header 'accept: application/json'

```
```
const axios = require('axios');

const url = 'https://api.trint.com/transcripts/?limit=100&skip=0';
const keyId = 'AK-12345ABCDE';
const keySecret = 'this15SECRET_CXJK3ctglt6LOpYxRmZ';

axios.get(url, {
    auth: {
        username: keyId,
        password: keySecret
    },
    headers: {
        accept: 'application/json'
    }
})
.then(response => {
    console.log("Response:", response.data);
})
.catch(error => {
    console.log("Failed to retrieve data:", error.response.status);
});
```
```
import requests
from requests.auth import HTTPBasicAuth

url = 'https://api.trint.com/transcripts/?limit=100&skip=0'
keyId = 'AK-12345ABCDE'
keySecret = 'this15SECRET_CXJK3ctglt6LOpYxRmZ'

headers = {
    'accept': 'application/json'
}

response = requests.get(url, auth=HTTPBasicAuth(keyId, keySecret), headers=headers)

if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Failed to retrieve data:", response.status_code)
```

You can see further examples of API calls in our [reference pages](https://dev.trint.com/reference/).
## Legacy Keys
For now we are continuing to support the use of old-style Trint API Keys (i.e. ones created before October 2024 that have a single value rather than a Key/Secret pair). These keys are still in use in some existing integrations (including Zapier) which will be migrated to the new system in the near future.
We recommend that all new API Keys are generated as Key/Secret pairs, but Legacy Keys can still be created using at the API tab in the webapp.
When using Legacy Keys, the value of the key must be sent as an `api-key` header parameter along with the existing request, for example:
#### Example Call using Legacy API Key
CurlJavascriptPython
```
curl --request GET  
     --url '<https://api.trint.com/transcripts/?limit=100&skip=0'>  
     --header 'accept: application/json'  
     --header 'api-key: LEGACY_API_KEY_GOES_HERE'
```
```
const axios = require('axios');

const url = 'https://api.trint.com/transcripts/?limit=100&skip=0';
const apiKey = 'LEGACY_API_KEY_GOES_HERE';

axios.get(url, {
    headers: {
        accept: 'application/json',
        'api-key: 'LEGACY_API_KEY_GOES_HERE'
    }
})
.then(response => {
    console.log("Response:", response.data);
})
.catch(error => {
    console.log("Failed to retrieve data:", error.response.status);
});
```
```
import requests

url = 'https://api.trint.com/transcripts/?limit=100&skip=0'
apiKey = 'LEGACY_API_KEY_GOES_HERE'

headers = {
    'accept': 'application/json',
    'api-key': 'LEGACY_API_KEY_GOES_HERE'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Failed to retrieve data:", response.status_code)
```

__Updated 5 months ago
* * *
[Trint API Pricing ](https://dev.trint.com/docs/pricing)
