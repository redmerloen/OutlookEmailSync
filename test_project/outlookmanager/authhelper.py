import base64
import json
import requests

from urllib import quote, urlencode

client_id = '#'
client_secret = '#'

authority = 'https://login.microsoftonline.com'

authorize_url = '%s/common/oauth2/v2.0/authorize?' % authority

token_url = '%s/common/oauth2/v2.0/token' % authority

scopes = ['openid',
          'profile',
          'https://outlook.office.com/mail.read']


def get_signin_url(redirect_uri):
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': ' '.join(str(i) for i in scopes)
    }

    signin_url = '%s%s' % (authorize_url, urlencode(params))

    return signin_url


def get_token_from_code(auth_code, redirect_uri):
    post_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(str(i) for i in scopes),
        'client_id': client_id,
        'client_secret': client_secret,
    }

    r = requests.post(token_url, data=post_data)

    try:
        return r.json()
    except:
        return 'Error retrieving token %s - %s' % (r.status_code, r.text)


def get_user_email_from_id_token(id_token):
    token_parts = id_token.split('.')
    encoded_token = token_parts[1]

    leftovers = len(encoded_token) % 4
    if leftovers == 2:
        encoded_token += '=='
    elif leftovers == 3:
        encoded_token += '='

    decoded = base64.urlsafe_b64decode(encoded_token.encode('utf-8')).decode('utf-8')
    print decoded

    jwt = json.loads(decoded)
    print jwt

    return jwt['preferred_username']
