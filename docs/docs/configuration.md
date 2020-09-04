# Configuration


## Create API Access

To use this module with the Zoho CRM, you will have to create a "Self-Client" API Access

1. Log in to [api-console.zoho.com](https://api-console.zoho.com)
2. Click "Add Client"
3. Select "Self-Client"
4. Copy the resulting "Client ID" and "Client Secret"


## Changing the Base URL

By default, the `ZohoCRMRestClient` connects to the `https://www.zohoapis.com` data center. This can be changed by setting the `.api_base_url` property:

```python
zohoclient = ZohoCRMRestClient()
zohoclient.api_base_url = 'https://accounts.zoho.eu'  # EU data center
```

[Zoho data center options can be viewed here.](https://www.zoho.com/crm/developer/docs/api/multi-dc.html)
