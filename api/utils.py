import os
import json
import logging
import requests
import dotenv

dotenv.load_dotenv()

HEADERS = {'Authorization': 'Basic {}'.format(os.environ.get('AUTH_1C'))}
BASE_URL_1C = os.environ.get('BASE_URL_1C')
DEBUG = os.environ.get('DEBUG', '') == 'True'


def make_request_to_1c(resourse, req):
    url = BASE_URL_1C + resourse
    try:
        res = requests.post(url, data=json.dumps(req, ensure_ascii=False).encode('utf-8'), headers=HEADERS,
                            verify=False)
        rt = res.json()
        if DEBUG:
            print('====================REQUEST====================')
            print(req)
            print('====================RESPONSE====================')
            print(res.text)
            print('====================END====================')
    except Exception as e:
        logger = logging.getLogger('vicidial')
        logger.error(f'1C error: {str(e)} res: {res.text}')
        rt = {'error': 'connection error'}
    return rt
