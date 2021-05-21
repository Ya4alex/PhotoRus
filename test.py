import requests
from pprint import pprint
import json
from requests.auth import HTTPBasicAuth

url = 'http://127.0.0.1:5000/api/morph_pars'
url2 = 'http://127.0.0.1:5000/api/get_token'

text2 = "Ну и тип! Но тут мистера Дурсля осенила мысль, что эти непонятные личности наверняка всего лишь собирают " \
        "пожертвования или что-нибудь в этом роде... "

par = {'text': text2}
token = requests.get(url2, auth=HTTPBasicAuth('YaAlex', '1')).json()
print(token)
r1 = requests.get(url=url, params=par, headers={'token': token['token']}, )

a = r1.json()

pprint(a)
