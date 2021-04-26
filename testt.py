import requests
from test2 import text
from pprint import pprint
import json

url = 'http://127.0.0.1:5000/api/morph_pars'

text2 = "Ну и тип! Но тут мистера Дурсля осенила мысль, что эти непонятные личности наверняка всего лишь собирают " \
        "пожертвования или что-нибудь в этом роде... "

par = {'text': text2}
r1 = requests.get(url=url, params=par)

a = r1.json()

pprint(a)
