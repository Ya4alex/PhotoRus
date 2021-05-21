import requests
from requests.auth import HTTPBasicAuth

par = {'text': text2}
token = requests.get(
    'http://127.0.0.1:5000/api/get_token',
    auth=HTTPBasicAuth('Username', 'Password'),
)
print(token.json())
