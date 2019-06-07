import requests
import json
import os


HEADERS = {'Authorization': 'Basic {}'.format(os.environ.get('AUTH_1C'))}
BASE_URL_1C = os.environ.get('BASE_URL_1C')


def make_request_to_1c(resourse, req):
    url = BASE_URL_1C + resourse
    try:
        rt = requests.post(url, data=json.dumps(req, ensure_ascii=False).encode('utf-8'), headers=HEADERS,
                           verify=False).text
        rt = json.loads(rt, encoding='utf-8-sig')
        print(rt)
    except:
        rt = {'error': 'connection error'}
    return rt
