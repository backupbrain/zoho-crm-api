import time
import requests
import json


class ZohoCRMOAuthToken:
    """Zoho access token."""

    access_token = None
    refresh_token = None
    api_domain = None
    token_type = None
    expires_in = None

    def __init__(self, json_data):
        """Initialize."""
        self.load_json(json_data)

    def load_json(self, json_data):
        """Convert from JSON."""
        self.access_token = json_data['access_token']
        self.api_domain = json_data['api_domain']
        self.token_type = json_data['token_type']
        self.expires_in = json_data['expires_in']
        if 'refresh_token' in json_data:
            self.refresh_token = json_data['refresh_token']

    def get_expiry_time_ms(self):
        """Get expiry time in MS."""
        return (self.expires_in * 1000) + self.get_current_time_ms()

    def get_current_time_ms(self):
        """Get current time in MS."""
        return round(time.time() * 1000)

    def is_expired(self):
        """Return True if this code is expired."""
        return self.get_current_time_ms() >= self.get_expiry_time_ms()


class ZohoCRMRestClient:
    """Zoho rest client."""

    api_base_url = 'https://www.zohoapis.com'
    api_version = 'v2'
    accounts_url = 'https://accounts.zoho.com'

    def get_client_id(self):
        """Return client ID."""
        return self.config['client_id']

    def get_client_secret(self):
        """Return client secret."""
        return self.config['client_secret']

    def get_redirect_uri(self):
        """Return redirect URI."""
        return self.config['redirect_uri']

    def generate_access_token(self, client_id, client_secret, grant_token, redirect_uri):
        """Generate access token."""
        url = '{accounts_url}/oauth/{api_version}/token'.format(
            accounts_url=self.accounts_url,
            api_version=self.api_version
        )
        post_parameters = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': grant_token,
        }
        response = requests.post(url, data=post_parameters)
        print(response.status_code)
        print(json.dumps(response.json(), indent=4))
        if response.status_code == 200:
            response_json = response.json()
            if 'error' not in response_json:
                access_token = ZohoCRMOAuthToken(response.json())
                return access_token
            else:
                raise ValueError(response_json['error'])
        else:
            raise ValueError(response_json['message'])

    def generate_refresh_token(self, client_id, client_secret, refresh_token):
        """Generate access token."""
        url = '{accounts_url}/oauth/{api_version}/token'.format(
            accounts_url=self.accounts_url,
            api_version=self.api_version
        )
        query_parameters = {
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token'
        }
        response = requests.post(url, params=query_parameters)
        print(response.status_code)
        print(json.dumps(response.json(), indent=4))
        if response.status_code == 200:
            response_json = response.json()
            if 'error' not in response_json:
                access_token = ZohoCRMOAuthToken(response.json())
                return access_token
            else:
                raise ValueError(response_json['error'])
        else:
            raise ValueError(response_json['message'])

    def is_logged_in(self, access_token):
        """Return true if access_token is active."""
        return access_token.is_expired() is False

    def api_fetch(self, access_token, endpoint, method='GET', headers=None, params=None, json_data=None):
        """Fetch from endpoint."""
        url = '{api_base_url}/crm/{api_version}/{endpoint}'.format(
            api_base_url=self.api_base_url,
            api_version=self.api_version,
            endpoint=endpoint
        )
        if headers is None:
            headers = {}
        headers['Authorization'] = 'Zoho-oauthtoken {}'.format(access_token)
        response = requests.request(
            method,
            url=url,
            headers=headers,
            params=params,
            json=json_data
        )
        print(response.status_code)
        print(json.dumps(response.json(), indent=4))
        return response


class ZohoCRMRecord:
    """Zoho Record."""

    record_type = ''
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

    def save(self, access_token):
        """Save contact."""
        if hasattr(self, 'id') and self.id is not None:
            self.update(access_token)
        else:
            self.insert(access_token)

    def insert(self, access_token):
        """Insert."""
        data = {}
        for property, value in vars(self).items():
            if property[0] != '_':
                data[property] = value
        print(json.dumps({'data': [data]}, indent=4))
        response = self._rest_client.api_fetch(
            access_token,
            'Contacts',
            method='POST',
            json_data={'data': [data]}
        )
        if response.status_code == 201:
            response_json = response.json()
            self.id = response_json['data'][0]['details']['id']
        else:
            raise ValueError(response.json()['message'])

    def update(self, access_token):
        """Update."""
        data = self.to_json()
        response = self._rest_client.api_fetch(
            access_token,
            'Contacts/{record_id}'.format(self.id),
            method='POST',
            json_data=data
        )
        if response.status_code != 201:
            raise ValueError(response.json()['message'])


class ZohoCRMUser(ZohoCRMRecord):
    """Zoho CRM User."""

    record_type = 'users'
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
            raise ValueError(response.json()['message'])

    def fetch_user(self, access_token, user_id):
        """Fetch User."""
        self.clear()
        response = self._rest_client.api_fetch(
            access_token,
            'users/{user_id}'.format(user_id),
        )
        if response.status_code == 200:
            self.from_json(response.json()['users'][0])
        else:
            raise ValueError(response.json()['message'])

    @staticmethod
    def fetch(zoho_rest_client, access_token, id):
        """Fetch by ID."""
        contact = ZohoCRMUser(zoho_rest_client)
        response = zoho_rest_client.api_fetch(
            access_token,
            '{record_type}/{id}'.format(record_type=ZohoCRMUser.record_type, id=id),
            method='GET'
        )
        if response.status_code == 200:
            contact.from_json(response.json()['data'][0])
            return contact
        else:
            raise ValueError(response.json()['message'])


class ZohoCRMContact(ZohoCRMRecord):
    """Zoho CRM Contact."""

    record_type = 'Contacts'

    @staticmethod
    def fetch(zoho_rest_client, access_token, id):
        """Fetch by ID."""
        contact = ZohoCRMContact(zoho_rest_client)
        response = zoho_rest_client.api_fetch(
            access_token,
            '{record_type}/{id}'.format(record_type=ZohoCRMContact.record_type, id=id),
            method='GET'
        )
        if response.status_code == 200:
            contact.from_json(response.json()['data'][0])
            return contact
        else:
            raise ValueError(response.json()['message'])


class ZohoCRMVendor(ZohoCRMRecord):
    """Zoho CRM Contact."""

    record_type = 'Vendors'

    @staticmethod
    def fetch(zoho_rest_client, access_token, id):
        """Fetch by ID."""
        contact = ZohoCRMContact(zoho_rest_client)
        response = zoho_rest_client.api_fetch(
            access_token,
            '{record_type}/{id}'.format(record_type=ZohoCRMVendor.record_type, id=id),
            method='GET'
        )
        if response.status_code == 200:
            contact.from_json(response.json()['data'][0])
            return contact
        else:
            raise ValueError(response.json()['message'])


class ZohoCRMLead(ZohoCRMRecord):
    """Zoho CRM Contact."""

    record_type = 'Leads'

    @staticmethod
    def fetch(zoho_rest_client, access_token, id):
        """Fetch by ID."""
        contact = ZohoCRMContact(zoho_rest_client)
        response = zoho_rest_client.api_fetch(
            access_token,
            '{record_type}/{id}'.format(record_type=ZohoCRMLead.record_type, id=id),
            method='GET'
        )
        if response.status_code == 200:
            contact.from_json(response.json()['data'][0])
            return contact
        else:
            raise ValueError(response.json()['message'])
