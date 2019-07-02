import os
import dotenv
import requests
import logging
from time import sleep
from celeryconfig import app_celery
from billiard.pool import Pool

fh = logging.FileHandler("vicidial.log")
fh.setFormatter(logging.Formatter('[%(asctime)s: %(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(fh)


@app_celery.task(name='add_lead')
def send_leads(leads):
    with Pool(10) as p:
        p.map(_send_lead, leads)


def _send_lead(lead):
    max_tries = 5
    dotenv.load_dotenv()
    url_for_load = os.environ.get('VICIDIAL_URL')
    resource = '/vicidial/non_agent_api.php'
    extended_data = {
        'action': 'add_unique_lead',
        'include_lists': lead.get('include_lists', ''),
        'exclude_statuses': lead.get('exclude_statuses', ''),
    }
    data = {
        'phone_number': lead.get('phone_number', ''),
        'list_id': lead.get('list_id', ''),
        'security_phrase': lead.get('security_phrase', ''),
        'address1': lead.get('address1', ''),
        'address2': lead.get('address2', ''),
        'province': lead.get('province', ''),
        'last_name': lead.get('last_name', ''),
        'postal_code': lead.get('postal_code', ''),
        'first_name': lead.get('first_name', ''),
        'phone_code': lead.get('phone_code', ''),
        'source': 'test',
        'user': os.environ.get('VICIDIAL_LOGIN'),
        'pass': os.environ.get('VICIDIAL_PASS'),
        'function': 'add_lead',
    }
    if lead.get('include_lists', None):
        data.update(extended_data)
        resource = '/non_agent_api_ext/index.php'
    for i in range(max_tries):
        try:
            response = requests.get(url_for_load + resource, params=data, verify=False)
            if response.status_code == 200:
                return
        except:
            if i < max_tries - 1:
                sleep(1)
            else:
                logger.error('Data add fail: ' + str(data))