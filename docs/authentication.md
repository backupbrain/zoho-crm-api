# Authentication

Zoho uses an OAuth authentication mechanism with a 60 minute timeout. The first access token must be authorized using a Grant Token, generated manually on the Zoho website and subsequent access tokens expire after 60 minutes and must be refreshed.


## Generating a Grant Token

1. Log in to [api-console.zoho.com](https://api-console.zoho.com)
2. Select "Self-Client"
3. Select your new "Self-Client" and generate a new grant token with your [desired scopes](https://www.zoho.com/crm/developer/docs/api/oauth-overview.html#scopes)
4. Copy that grant token

## Generating an Access Token


```python
from zohocrm import ZohoCRMRestClient

client_id = '<paste your Zoho client id>'
client_secret = '<paste your Zoho client secret>'
redirect_uri = '<paste your Redirect URL>'
grant_token = '<paste your newly created token>'
zoho_client = ZohoCRMRestClient(client_id, client_secret, redirect_uri)

#  generate your oauth token
oauth_access_token = zoho_client.generate_access_token(grant_token)

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

zoho_client = ZohoCRMRestClient(client_id, client_secret, redirect_uri)
zoho_client.oauth_access_token = ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>",
    "api_domain": zoho_client.api_base_url,
    "token_type": "Bearer",
    "expiry_timestamp": <expiration_timestamp_float>
})
```

## Refreshing Tokens

Zoho access tokens are valid for 60 minutes, so they must be  refreshed periodically. This can be done manually or in a thread or a cron.

```python
# ...
#  refresh your oauth token
oauth_refresh_token = zoho_client.generate_refresh_token()

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

zoho_client = ZohoCRMRestClient(client_id, client_secret, redirect_uri)
zoho_client.oauth_access_token = ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>",
    "api_domain": zoho_client.api_base_url,
    "token_type": "Bearer",
    "expiry_timestamp": <expiration_timestamp_float>
})

zoho_client.oauth_refresh_token = ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expiry_timestamp": <expiration_timestamp_float>
})
```


```python
from zohocrm import ZohoCRMRestClient, ZohoCRMOAuthToken

zoho_client = ZohoCRMRestClient(client_id, client_secret, redirect_uri)
zoho_client.oauth_access_token = ZohoCRMOAuthToken({
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expiry_timestamp": <expiration_timestamp_float>
})
```