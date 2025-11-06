---
source: https://dev.trint.com/docs/us-vs-eu-tenant
retrieved: 2025-11-06T03:44:37.793354+00:00
---

# US vs EU Tenant
How to know if your account is on the EU tenant, and what your links should look like if you are.
## 
Trint Tenants
[](https://dev.trint.com/docs/us-vs-eu-tenant#trint-tenants)
Trint has two entirely separate customer facing tenants, one in the US and one in the EU. User accounts on one tenant will not work in the other tenant - you will be able to tell which tenant you are a member of by checking the URL that you log in with. US tenant customers will log in at <https://app.trint.com> while EU tenant customers log in at <https://app.eu.trint.com>
## 
US vs EU endpoints
[](https://dev.trint.com/docs/us-vs-eu-tenant#us-vs-eu-endpoints)
The API URLs for the two tenants follow the same scheme as the above login link.
If you are using the API for the US tenant, you will be using URLs based on the https://*.trint.com pattern.
If you are using the API for the EU tenant, you will be using URLs based on the https://*.eu.trint.com pattern.
### 
US endpoints:
[](https://dev.trint.com/docs/us-vs-eu-tenant#us-endpoints)
  * <https://upload.trint.com/>
  * <https://api.trint.com/>


### 
EU endpoints:
[](https://dev.trint.com/docs/us-vs-eu-tenant#eu-endpoints)
  * <https://upload.eu.trint.com/>
  * <https://api.eu.trint.com/>


Example call to list Trint on the EU API:
CurlJavascriptPython
```
curl --request GET \
     -u "AK-12345ABCDE:this15SECRET_CXJK3ctglt6LOpYxRmZ"
     --url 'https://api.eu.trint.com/transcripts/?limit=100&skip=0' \
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

response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=headers)

if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Failed to retrieve data:", response.status_code)
```

__Updated 5 months ago
* * *
[Webhooks](https://dev.trint.com/docs/receiving-callback-notifications)[SCIM API and Trint ](https://dev.trint.com/docs/scim)
  * [__Table of Contents](https://dev.trint.com/docs/us-vs-eu-tenant)
  *     * [Trint Tenants](https://dev.trint.com/docs/us-vs-eu-tenant#trint-tenants)
    * [US vs EU endpoints](https://dev.trint.com/docs/us-vs-eu-tenant#us-vs-eu-endpoints)
    *       * [US endpoints:](https://dev.trint.com/docs/us-vs-eu-tenant#us-endpoints)
      * [EU endpoints:](https://dev.trint.com/docs/us-vs-eu-tenant#eu-endpoints)
