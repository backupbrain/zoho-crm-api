import time
import requests
# import json


class ZohoCRMOAuthToken:
    """Zoho access token."""

    access_token = None
    refresh_token = None
    api_domain = None
    token_type = None
    expiry_timestamp = None

    def __init__(self, json_data):
        """Initialize."""
        self.load_json(json_data)

    def to_json(self):
        """Output to JSON."""
        data = {
            'access_token': self.access_token,
            'api_domain': self.api_domain,
            'token_type': self.token_type,
            'expiry_timestamp': self.expiry_timestamp,
        }
        if self.refresh_token is not None:
            data['refresh_token'] = self.refresh_token
        return data

    def load_json(self, json_data):
        """Convert from JSON."""
        self.access_token = json_data['access_token']
        self.api_domain = json_data['api_domain']
        self.token_type = json_data['token_type']
        if 'expires_in' in json_data:
            self.expiry_timestamp = json_data['expires_in'] + time.time()
        if 'expiry_timestamp' in json_data:
            self.expiry_timestamp = json_data['expiry_timestamp']
        if 'refresh_token' in json_data:
            self.refresh_token = json_data['refresh_token']

    def is_expired(self):
        """Return True if this code is expired."""
        return time.time() >= self.expiry_timestamp


class ZohoCRMRestClient:
    """Zoho rest client."""

    api_base_url = 'https://www.zohoapis.com'
    api_version = 'v2'
    accounts_url = 'https://accounts.zoho.com'

    client_id = None
    client_secret = None
    redirect_uri = None

    oauth_access_token = None
    oauth_refresh_token = None

    def __init__(self, client_id, client_secret, redirect_uri):
        """Initialize REST client."""
        self.client_id = client_id,
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def generate_access_token(self, grant_token):
        """Generate access token."""
        url = '{accounts_url}/oauth/{api_version}/token'.format(
            accounts_url=self.accounts_url,
            api_version=self.api_version
        )
        post_parameters = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': grant_token,
        }
        response = requests.post(url, data=post_parameters)
        # print(response.status_code)
        # print(json.dumps(response.json(), indent=4))
        if response.status_code == 200:
            response_json = response.json()
            if 'error' not in response_json:
                access_token = ZohoCRMOAuthToken(response.json())
                self.oauth_access_token = access_token
                return access_token
            else:
                raise ValueError(response_json['error'])
        else:
            raise ValueError(response_json['message'])

    def generate_refresh_token(self):
        """Generate access token."""
        url = '{accounts_url}/oauth/{api_version}/token'.format(
            accounts_url=self.accounts_url,
            api_version=self.api_version
        )
        query_parameters = {
            'refresh_token': self.oauth_access_token.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }
        response = requests.post(url, params=query_parameters)
        # print(response.status_code)
        # print(json.dumps(response.json(), indent=4))
        if response.status_code == 200:
            response_json = response.json()
            if 'error' not in response_json:
                access_token = ZohoCRMOAuthToken(response.json())
                self.oauth_refresh_token = access_token
                return access_token
            else:
                raise ValueError(response_json['error'])
        else:
            raise ValueError(response_json['message'])

    def is_logged_in(self, access_token):
        """Return true if access_token is active."""
        return access_token.is_expired() is False

    def api_fetch(self, endpoint, method='GET', headers=None, params=None, json_data=None):
        """Fetch from endpoint."""
        url = '{api_base_url}/crm/{api_version}/{endpoint}'.format(
            api_base_url=self.api_base_url,
            api_version=self.api_version,
            endpoint=endpoint
        )
        if headers is None:
            headers = {}
        if self.oauth_refresh_token is None:
            headers['Authorization'] = 'Zoho-oauthtoken {}'.format(self.oauth_access_token.access_token)
        else:
            headers['Authorization'] = 'Zoho-oauthtoken {}'.format(self.oauth_refresh_token.access_token)
        response = requests.request(
            method,
            url=url,
            headers=headers,
            params=params,
            json=json_data
        )
        # print(response.status_code)
        # print(json.dumps(response.json(), indent=4))
        return response


class ZohoCRMRecord:
    """Zoho Record."""

    _module_name = ''
    _rest_client = None

    def __init__(self, zoho_rest_client):
        """Initialize."""
        self._rest_client = zoho_rest_client

    def clear(self):
        """Clean the object."""
        for property, value in vars(self).items():
            if property[0] != '_':
                setattr(self, property, None)

    def to_json(self):
        """To JSON."""
        data = {}
        for property, value in vars(self).items():
            if property[0] != '_':
                data[property] = value
        return data

    def from_json(self, json_data):
        """From JSON."""
        for key, value in json_data.items():
            setattr(self, key, value)

    def save(self):
        """Save contact."""
        if hasattr(self, 'id') and self.id is not None:
            self.update()
        else:
            self.insert()

    def insert(self):
        """Insert."""
        data = {}
        for property, value in vars(self).items():
            if property[0] != '_':
                data[property] = value
        # print(json.dumps({'data': [data]}, indent=4))
        response = self._rest_client.api_fetch(
            '{module_name}'.format(module_name=self._module_name),
            method='POST',
            json_data={'data': [data]}
        )
        if response.status_code == 201:
            response_json = response.json()
            self.id = response_json['data'][0]['details']['id']
        else:
            response_json = response.json()
            if 'data' in response_json:
                raise ValueError(response_json['data'][0]['message'])
            else:
                raise ValueError(response_json['message'])

    def update(self):
        """Update."""
        data = self.to_json()
        response = self._rest_client.api_fetch(
            '{module_name}/{record_id}'.format(module_name=self._module_name, record_id=self.id),
            method='PUT',
            json_data={'data': [data]}
        )
        if response.status_code != 200:
            response_json = response.json()
            if 'data' in response_json:
                raise ValueError(response_json['data'][0]['message'])
            else:
                raise ValueError(response_json['message'])

    def delete(self):
        """Delete."""
        response = self._rest_client.api_fetch(
            '{module_name}/{record_id}'.format(module_name=self._module_name, record_id=self.id),
            method='DELETE'
        )
        if response.status_code == 200:
            self.id = None
        else:
            response_json = response.json()
            if 'data' in response_json:
                raise ValueError(response_json['data'][0]['message'])
            else:
                raise ValueError(response_json['message'])

    @classmethod
    def fetch(cls, zoho_rest_client, id):
        """Fetch by ID."""
        print(cls._module_name)
        obj = cls(zoho_rest_client)
        response = zoho_rest_client.api_fetch(
            '{module_name}/{id}'.format(module_name=cls._module_name, id=id),
            method='GET'
        )
        if response.status_code == 200:
            obj.from_json(response.json()['data'][0])
            return obj
        else:
            response_json = response.json()
            if 'data' in response_json:
                raise ValueError(response_json['data'][0]['message'])
            else:
                raise ValueError(response_json['message'])

    @classmethod
    def delete_id(cls, zoho_rest_client, id):
        """Delete from ID."""
        response = zoho_rest_client.api_fetch(
            '{module_name}/{record_id}'.format(module_name=cls._module_name, record_id=id),
            method='DELETE'
        )
        if response.status_code != 200:
            response_json = response.json()
            if 'data' in response_json:
                raise ValueError(response_json['data'][0]['message'])
            else:
                raise ValueError(response_json['message'])


class ZohoCRMUser(ZohoCRMRecord):
    """Zoho CRM User."""

    _module_name = 'users'
    _rest_client = None

    def fetch_current_user(self, access_token):
        """Fetch current User."""
        self.clear()
        response = self._rest_client.api_fetch(
            access_token,
            'users',
            params={
                'type': 'CurrentUser'
            }
        )
        if response.status_code == 200:
            self.from_json(response.json()['users'][0])
        else:
            response_json = response.json()
            if 'data' in response_json:
                raise ValueError(response_json['data'][0]['message'])
            else:
                raise ValueError(response_json['message'])

    def fetch_user(self, access_token, user_id):
        """Fetch User."""
        self.clear()
        response = self._rest_client.api_fetch(
            access_token,
            'users/{user_id}'.format(user_id=user_id),
        )
        if response.status_code == 200:
            self.from_json(response.json()['users'][0])
        else:
            response_json = response.json()
            if 'data' in response_json:
                raise ValueError(response_json['data'][0]['message'])
            else:
                raise ValueError(response_json['message'])


class ZohoCRMContact(ZohoCRMRecord):
    """Zoho CRM Contact."""

    _module_name = 'Contacts'


class ZohoCRMVendor(ZohoCRMRecord):
    """Zoho CRM Vendor."""

    _module_name = 'Vendors'


class ZohoCRMLead(ZohoCRMRecord):
    """Zoho CRM Lead."""

    _module_name = 'Leads'


class ZohoCRMAccount(ZohoCRMRecord):
    """Zoho CRM Account."""

    _module_name = 'Deal'


class ZohoCRMDeal(ZohoCRMRecord):
    """Zoho CRM Account."""

    _module_name = 'Deals'


class ZohoCRMCampaign(ZohoCRMRecord):
    """Zoho CRM Campaign."""

    _module_name = 'Campaigns'


class ZohoCRMTask(ZohoCRMRecord):
    """Zoho CRM Task."""

    _module_name = 'Tasks'


class ZohoCRMCase(ZohoCRMRecord):
    """Zoho CRM Case."""

    _module_name = 'Cases'


class ZohoCRMEvent(ZohoCRMRecord):
    """Zoho CRM Event."""

    _module_name = 'Events'


class ZohoCRMCall(ZohoCRMRecord):
    """Zoho CRM Call."""

    _module_name = 'Calls'


class ZohoCRMSolution(ZohoCRMRecord):
    """Zoho CRM Solution."""

    _module_name = 'Solutions'


class ZohoCRMProduct(ZohoCRMRecord):
    """Zoho CRM Product."""

    _module_name = 'Products'


class ZohoCRMQuote(ZohoCRMRecord):
    """Zoho CRM Quote."""

    _module_name = 'Quotes'


class ZohoCRMInvoice(ZohoCRMRecord):
    """Zoho CRM Invoice."""

    _module_name = 'Invoices'


class ZohoCRMCustom(ZohoCRMRecord):
    """Zoho CRM Custom."""

    _module_name = 'Custom'


class ZohoCRMActivity(ZohoCRMRecord):
    """Zoho CRM Activity."""

    _module_name = 'Activities'


class ZohoCRMPriceBook(ZohoCRMRecord):
    """Zoho CRM Price Book."""

    _module_name = 'pricebooks'


class ZohoCRMSalesOrder(ZohoCRMRecord):
    """Zoho CRM Sales Order."""

    _module_name = 'salesorders'


class ZohoCRMPurchaseOrder(ZohoCRMRecord):
    """Zoho CRM Purchase Order."""

    _module_name = 'purchaseorders'


class ZohoCRMNote(ZohoCRMRecord):
    """Zoho CRM Note."""

    _module_name = 'notes'
