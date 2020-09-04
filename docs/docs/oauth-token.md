# The ZohoCRMOAuthToken Object

When you create or refresh an oauth_token, the `ZohoCRMRestClient` will return a `ZohoCRMOAuthToken` instance.

The `ZohoCRMOAuthToken` contains:

* an `.access_token`, which is used to authorize API access
* `.is_expired()`, which returns `True` if the access token is expired

If the  `ZohoCRMOAuthToken` was created with the `zoho_client.generate_access_token` method, it will also contain:

* `.refresh_token`, which must be used for all future token refresh requests using the `zoho_client.generate_refresh_token()` method.
