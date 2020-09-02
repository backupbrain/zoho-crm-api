
# Zoho CRM API
This API is for people who are having trouble with the official Zoho API.


## Installation

You can install 
```
$ cd <python-project-folder>
$ git clone https://github.com/backupbrain/zoho-crm-api.git
```

## Usage

### Set-up

1) Log in to [api-console.zoho.com](https://api-console.zoho.com)
2) Click "Add Client"
3) Select  "Server-based Application" or "Self-Client"
4) Select your new "Self-Client" or "Server-based Application" and generate a new grant token with your [desired scopes](https://www.zoho.com/crm/developer/docs/api/oauth-overview.html#scopes)
5) Copy that grant token

### Log-in 


```python
from zoho-crm-api import ZohoCRMRestClient

client_id = '<paste your Zoho client id>'
client_secret = '<paste your Zoho client secret>'
redirect_uri = '<paste your Redirect URL>'
grant_token = '<paste your newly created token>'
zohoclient = ZohoCRMRestClient()

#  generate your oauth token
oauth_token = zohoclient.generate_access_token(
    client_id,
    client_secret,
    grant_token,
    redirect_uri
)

# returns a ZohoCRMOAuthToken instance:
'''
ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>,
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expires_in": 3600
})
'''

# oauth_token.refresh_token is used to refresh the token
# oauth_token.access_token is used to authorize future interacitons with the API
# oauth_token.is_expired() returns true when the token has expired
```

### Refresh 

Zoho access tokens are valid for 60 minutes, so they must be  refreshed periodically. This can be done manually or in a thread or a cron.

```python
# ...
#  refresh your oauth token
oauth_refresh_token = zohoclient.generate_refresh_token(
    client_id,
    client_secret,
    oauth_token.refresh_token
)

# returns a ZohoCRMOAuthToken instance:
'''
ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expires_in": 3600
})
'''
# oauth_refresh_token.access_token is used to authorize future interacitons with the API
# oauth_refresh_token.is_expired() returns true when the token has expired
```

### The ZohoCRMOAuthToken Object

When you create or refresh an oauth_token, the `ZohoCRMRestClient` will return a `ZohoCRMOAuthToken` instance.

The `ZohoCRMOAuthToken` contains:
* an `.access_token`, which is used to authorize future API access
* `.is_expired()`, which returns `True` if the access token is expired

If the  `ZohoCRMOAuthToken` was created with the `zohoclient.generate_access_token` method, it will also contain:
* `.refresh_token`, which must be used for all future token refresh requests using the `zohoclient.generate_refresh_token()` method.

### Working with Contacts

Import the `ZohoCRMContact` module

```python
from zoho-crm-api import ZohoCRMContact
```

#### Retrieve a contact

```python
contact_id = 1234023423424
contact = ZohoCRMContact.fetch(
    zohoclient,
    refresh_token.access_token,
    contact_id
)
```

#### Insert or Update a Contact

```python
owner = {
    'id': 1234234234,
    'name': "<Your user's name>",
    'email': "<Your user's email>"
}
contact = ZohoCRMContact(zohoclient)
contact.First_Name = 'John'
contact.Last_Name = 'Doe'
contact.Title = 'Job title'
contact.Company = 'Programming'
contact.Industry = 'San Francisco'
contact.State = 'CA'
contact.Country = 'United States'
contact.ZIP_Code = '94110'
contact.Website = 'http://example.com'
contact.Owner = owner

# if contact.id is set, .save() will update
# if contact.id is not set, .save() will insert
contact.save(refresh_token.access_token)
```


### Working with Vendors

Import the `ZohoCRMVendor` module

```python
from zoho-crm-api import ZohoCRMVendor
```

#### Retrieve a Vendor

```python
vendor_id = 1234023423424
contact = ZohoCRMVendor.fetch(
    zohoclient,
    refresh_token.access_token,
    vendor_id
)
```

#### Insert or Update a Vendor

Inserting  and updating a `ZohoCRMVendor` is the  same as with a `ZohoCRMContact`,  but with Vendor data instead of Contact data.

### Working with Leads

Import the `ZohoCRMLead` module

```python
from zoho-crm-api import ZohoCRMLead
```

#### Retrieve a Lead

```python
lead_id = 1234023423424
contact = ZohoCRMLead.fetch(
    zohoclient,
    refresh_token.access_token,
    vendor_id
)
```

#### Insert or Update a Lead

Inserting and updating a `ZohoCRMLead` is the same as with a `ZohoCRMContact`,  but with Lead data instead of Contact data.