import os
import dotenv
import requests
import logging
from time import sleep, timezone
from celeryconfig import app_celery

fh = logging.FileHandler("vicidial.log")
fh.setFormatter(logging.Formatter(
    '[%(asctime)s: %(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(fh)


@app_celery.task(name='update_lead')
def update_lead(lead):
    dotenv.load_dotenv()
    url_for_load = os.environ.get('VICIDIAL_URL')
    resource = "/vicidial/non_agent_api.php"
    lead.pop('type')
    lead['function'] = 'update_lead'
    lead['user'] = os.environ.get('VICIDIAL_LOGIN')
    lead['pass'] = os.environ.get('VICIDIAL_PASS')
    lead['source'] = 'test'

    requests.get(
        url_for_load + resource,
        params=lead,
        verify=False)


@app_celery.task(name='add_lead')
def send_leads(leads):
    for lead in leads:
        _send_lead(lead)


def _send_lead(lead):
    max_tries = 5
    dotenv.load_dotenv()
    DEBUG = os.environ.get('ENABLE_LOG', '') == 'True'
    url_for_load = os.environ.get('VICIDIAL_URL')
    resource = '/vicidial/non_agent_api.php'  # may will override later
    data = {
        'phone_number': lead.get('phone_number', ''),
        'list_id': lead.get('list_id', ''),
        'security_phrase': lead.get('security_phrase', ''),
        'address1': lead.get('address1', ''),
        'address2': lead.get('address2', ''),
        'address3': lead.get('address3', ''),
        'province': lead.get('province', ''),
        'last_name': lead.get('last_name', ''),
        'postal_code': lead.get('postal_code', ''),
        'city': lead.get('city', ''),
        'email': lead.get('email', ''),
        'first_name': lead.get('first_name', ''),
        'phone_code': lead.get('phone_code', ''),
        'source': 'test',
        'user': os.environ.get('VICIDIAL_LOGIN'),
        'pass': os.environ.get('VICIDIAL_PASS'),
        'gmt_offset_now': f'{round(-timezone/3600)}',
        'function': 'add_lead',
    }
    if lead.get('include_lists', None):
        data.update({
            'action': 'add_unique_lead',
            'include_lists': lead.get('include_lists', ''),
            'exclude_statuses': lead.get('exclude_statuses', ''),
        })
        resource = '/non_agent_api_ext/index.php'
    if lead.get('callback', None):
        data.update({
            'callback': 'Y',
            'callback_status': 'CALLBK',
            'campaign_id': 'ccMain',
            'callback_datetime': lead.get('callback_datetime', lead.get('security_phrase', '')),
            'callback_comments': lead.get('callback_comments', ''),
        })
    for i in range(max_tries):
        try:
            if DEBUG:
                logger.info(f'Try load {data.get("phone_number")}')
            response = requests.get(
                url_for_load + resource,
                params=data,
                verify=False)
            if DEBUG:
                logger.info(
                    f'{data.get("phone_number")}: {response.status_code} - {response.reason}')
            if response.status_code == 200:
                return
        except Exception as e:
            if DEBUG:
                logger.error(str(e))
            if i < max_tries - 1:
                sleep(1)
            else:
                logger.error('Data add fail: ' + str(data))
