# PhotoRus
*Rest-API server*
 
## Документация API

Авторизация `/api/get_token`
Для работы с ресурсами необходимо иметь токен который можно получить, пройдя регистрацию.
Пример на requests:

    import requests
    from requests.auth import HTTPBasicAuth
    
    token = requests.get(
        'http://127.0.0.1:5000/api/get_token',
        auth=HTTPBasicAuth('Username', 'Password'),
    )
    print(token.json())

В запросах токен указывается в заголовке `token`.

###### Пример с применением токена:

```python
import requests

request = requests.get(
    url='http://127.0.0.1:5000/api/morph_pars',
    params=params,
    headers={'token': token}
)
```

Синтаксический разбор предложения `/api/syntactic_parsing`
Возвращает словарь в формате .json c синтаксическим анализом предложений. Для работы нужен токен, иначе вернет `401`.
Параметры запроса:
- `text` (str) обязательный оргумент c текстом. Если в тексте больше одного предложения, они будут разделены
- `check_grammar` (bool) не обязательный аргумент. Испраить грамматические ошибки и опечатки. Значительно увеличивается время обработки запроса.

###### Формат ответа:

```json
[
    {
        "content":
            [
                {
                    "feathers": {
                        "feats": {
                            "Case": "Nom",
                            "Number": "Sing",
                            "Person": "1"
                        },
                        "natasha_tag": "nsubj",
                        "obj": "NPRO",
                        "photorus_tag": "подлежащее",
                        "set": {
                            "Case": "Nom",
                            "Mood": None
                        }
                    },
                    "relations": {
                        "group": {
                            "human_tag": "основная группа",
                            "tag": "root"
                        },
                        "head_id": 1,
                        "id": 0,
                        "m_head_id": 1
                    },
                    "word": "Я"
                },
                {'''другое слово'''},
                {'''ещё слово'''},
                {'''точка'''},
            ],
        "sent": "Я люблю майнкрафт."
    },
    {'''другое предложение'''}
]
```