import base64, requests
from skillbase_api import settings

API_ENDPOINT = 'https://discord.com/api/v8'

def get_token(code, redirect_uri):
  data = {
    'grant_type': 'authorization_code',
    'code': code,
    'client_id': settings.OAUTH_CLIENT,
    'client_secret': settings.OAUTH_SECRET,
    'scope': 'identify',
    'redirect_uri': redirect_uri,
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
  print(code)
  print(r.text)
  r.raise_for_status()
  return r.json()['access_token']

def get_user(code):
    headers = {
        'Authorization': f'Bearer {code}'
    }
    r = requests.get('%s/oauth2/@me' % API_ENDPOINT, headers=headers)
    r.raise_for_status()
    return r.json()['user']
