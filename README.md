

# Zoho CRM API
This API is for people who are having trouble with the official Zoho API. 

* Supports Zoho API v2

So far this package supports the following Record API actions:

| Module          | Create | Retrieve | Update | Delete |
|-----------------|--------|----------|--------|--------|
| Contacts        | x      | x        | x      | x      |
| Leads           | x      | x        | x      | x      |
| Vendors         | x      | x        | x      | x      |
| Accounts        | x      | x        | x      | x      |
| Deals           | x      | x        | x      | x      |
| Vendors         | x      | x        | x      | x      |
| Campaign        | x      | x        | x      | x      |
| Tasks           | x      | x        | x      | x      |
| Cases           | x      | x        | x      | x      |
| Calls           | x      | x        | x      | x      |
| Solutions       | x      | x        | x      | x      |
| Products        | x      | x        | x      | x      |
| Vendors         | x      | x        | x      | x      |
| Price Books     | x      | x        | x      | x      |
| Quotes          | x      | x        | x      | x      |
| Sales Orders    | x      | x        | x      | x      |
| Purchase Orders | x      | x        | x      | x      |
| Invoices        | x      | x        | x      | x      |
| Custom          | x      | x        | x      | x      |
| Notes           | x      | x        | x      | x      |
| Activities      | x      | x        | x      | x      |


## Installation

You can install from pip:
```
$ pip install zohocrmapi
```

Or from Github:

```
$ cd <python-project-folder>
$ git clone https://github.com/backupbrain/zoho-crm-api
$ ln -s zoho-crm-api/zohocrm zohocrm
$ pip install -r zoho-crm-api/requirements.txt  # install requirements
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
from zohocrm import ZohoCRMRestClient

client_id = '<paste your Zoho client id>'
client_secret = '<paste your Zoho client secret>'
redirect_uri = '<paste your Redirect URL>'
grant_token = '<paste your newly created token>'
zohoclient = ZohoCRMRestClient(client_id, client_secret, redirect_uri)

#  generate your oauth token
oauth_access_token = zohoclient.generate_access_token(grant_token)

# returns a ZohoCRMOAuthToken instance:
'''
ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expiry_timestamp": <expiration timestamp float>
})
'''

# oauth_access_token.refresh_token is used to refresh the token
# oauth_access_token.access_token is used to authorize future interacitons with the API
# oauth_access_token.is_expired() returns true when the token has expired
```

The `oauth_access_token` is saved for future use, for instance for accessing restricted areas of the API or for refreshing the OAuth token.

In cases where the OAuth  token must be loaded manually, for instance in a cron job that asks to refresh the token, the ZohoCRMOAuthToken can be loaded manually:

```python
from zohocrm import ZohoCRMRestClient, ZohoCRMOAuthToken

zohoclient = ZohoCRMRestClient(client_id, client_secret, redirect_uri)
zohoclient.oauth_access_token = ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expiry_timestamp": <expiration_timestamp_float>
})
```

### Refresh 

Zoho access tokens are valid for 60 minutes, so they must be  refreshed periodically. This can be done manually or in a thread or a cron.

```python
# ...
#  refresh your oauth token
oauth_refresh_token = zohoclient.generate_refresh_token()

# returns a ZohoCRMOAuthToken instance:
'''
ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expiry_timestamp": <expiration timestamp float>
})
'''
# oauth_refresh_token.access_token is used to authorize future interacitons with the API
# oauth_refresh_token.is_expired() returns true when the token has expired
```

The `oauth_refresh_token` is saved for future use, for instance for accessing restricted areas of the API or for refreshing the OAuth token.

In cases where the OAuth  token must be loaded manually, for instance in a cron job that asks to refresh the token, the both the `.oauth_access_token` and `.oauth_refresh_token` must be loaded manually, because:
* the `.oauth_access_token` contains the `.refresh_token`, required for refreshing the OAuth token:
* the `.oauth_refresh_token` contains  the latest  `.access_token` generated by the Zoho API, required for accessing restricted areos of the API.


```python
from zohocrm import ZohoCRMRestClient, ZohoCRMOAuthToken

zohoclient = ZohoCRMRestClient(client_id, client_secret, redirect_uri)
zohoclient.oauth_access_token = ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expiry_timestamp": <expiration_timestamp_float>
})

zohoclient.oauth_refresh_token = ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expiry_timestamp": <expiration_timestamp_float>
})
```


```python
from zohocrm import ZohoCRMRestClient, ZohoCRMOAuthToken

zohoclient = ZohoCRMRestClient(client_id, client_secret, redirect_uri)
zohoclient.oauth_access_token = ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expiry_timestamp": <expiration_timestamp_float>
})
```

### The ZohoCRMOAuthToken Object

When you create or refresh an oauth_token, the `ZohoCRMRestClient` will return a `ZohoCRMOAuthToken` instance.

The `ZohoCRMOAuthToken` contains:
* an `.access_token`, which is used to authorize API access
* `.is_expired()`, which returns `True` if the access token is expired

If the  `ZohoCRMOAuthToken` was created with the `zohoclient.generate_access_token` method, it will also contain:
* `.refresh_token`, which must be used for all future token refresh requests using the `zohoclient.generate_refresh_token()` method.

### Changing the Base URL

By default, the `ZohoCRMRestClient` connects to the `https://www.zohoapis.com` data center. This can be changed by setting the `.api_base_url` property:

```python
zohoclient = ZohoCRMRestClient()
zohoclient.api_base_url = 'https://accounts.zoho.eu'  # EU data center
```

[Zoho data center options can be viewed here.](https://www.zoho.com/crm/developer/docs/api/multi-dc.html)


### Working with Contacts

Import the `ZohoCRMContact` module

```python
from zohocrm import ZohoCRMContact
```

#### Retrieve a contact

```python
contact_id = 1234023423424
contact = ZohoCRMContact.fetch(
    zohoclient,
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
contact.save()
```

#### Delete a Contact

You can delete a contact with or without retrieving it first.

If the contact has already  been retrieved, the `.delete()` method will delete the record with the matching `.id`:

```python
contact_id = 1234023423424
contact = ZohoCRMContact.fetch(
    zohoclient,
    contact_id
)

# Delete
contact.delete()
```

If the contact has not yet been retrieved, the `.delete_id()` requires the `id` of the record and can be called from the static class:

```python
contact_id = 1234023423424
contact = ZohoCRMContact.delete_id(
    zohoclient,
    contact_id
)
```


### Working with Vendors

Import the `ZohoCRMVendor` module

```python
from zohocrm import ZohoCRMVendor
```

#### Retrieve a Vendor

```python
vendor_id = 1234023423424
contact = ZohoCRMVendor.fetch(
    zohoclient,
    vendor_id
)
```

#### Insert or Update a Vendor

Inserting  and updating a `ZohoCRMVendor` is the  same as with a `ZohoCRMContact`,  but with Vendor data instead of Contact data.

### Working with Leads

Import the `ZohoCRMLead` module

```python
from zohocrm import ZohoCRMLead
```

#### Delete a Lead

You can delete a contact with or without retrieving it first.

If the lead has already been retrieved, the `.delete()` method will delete the record with the matching `.id`:

```python
lead_id = 1234023423424
lead = ZohoCRMLead.fetch(
    zohoclient,
    lead_id
)

# Delete
lead.delete()
```

If the lead has not yet been retrieved, the `.delete_id()` requires the `id` of the record and can be called from the static class:

```python
lead_id = 1234023423424
contact = ZohoCRMLead.delete_id(
    zohoclient,
    lead_id
)
```


#### Retrieve a Lead

```python
lead_id = 1234023423424
contact = ZohoCRMLead.fetch(
    zohoclient,
    vendor_id
)
```

#### Insert or Update a Lead

Inserting and updating a `ZohoCRMLead` is the same as with a `ZohoCRMContact`,  but with Lead data instead of Contact data.

#### Delete a Lead

Deleting a `ZohoCRMLead` is the same as with a `ZohoCRMContact`,  but with Lead data instead of Contact data.

#### Other modules

The API interface is the same for all [Zoho Records](https://www.zoho.com/crm/developer/docs/api/get-records.html).