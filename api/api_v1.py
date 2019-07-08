import os
import requests
import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from .utils import make_request_to_1c
from tasks import send_leads

logger = logging.getLogger('vicidial')
api = Blueprint('api', __name__)
allowed_actions = ('send_sms', 'get_payment_requsits', 'get_main_info', 'get_loan_info', 'get_ticket_info',
                   'get_detail_loan', 'get_detail_ticket', 'find_by_fio', 'get_loans_by_phone', 'get_balance_on_date',
                   'get_phones_from_order')

another_actions = ('get_lk_info',)


@api.route('/ivr', methods=['GET', 'POST'])
@cross_origin()
def get_ivr_info():
    auth_key = request.headers.get('X-Auth-Key', '')
    if auth_key != os.environ.get('AUTH_KEY'):
        return jsonify(error='Not authenticated')
    source = request.args if request.method == 'GET' else request.get_json()

    phone = source.get('phone', '')
    inn = source.get('inn', '')
    send_sms = bool(source.get('sendsms', False))
    if phone or inn:
        response = make_request_to_1c('ivr', {'phone': phone, 'inn': inn, 'send_sms': send_sms})
        return jsonify(response)
    return jsonify(error='source undefined')


@api.route('/vicidial/<action>', methods=['POST'])
@cross_origin()
def vicidial_handler(action):
    auth_key = request.headers.get('X-Auth-Key', '')
    if auth_key != os.environ.get('AUTH_KEY'):
        return jsonify(error='Not authenticated')

    try:
        data = request.get_json()
    except:
        return jsonify(error='data not json')

    data['action'] = action
    if action in allowed_actions:
        response = make_request_to_1c('vicidial', data)
    elif action in another_actions:
        gt_token = os.environ.get('AUTH_GETAWAY_TOKEN')
        gt_url = os.environ.get('GETAWAY_URL')
        data = {
            'flag_get': 'get_info_vici',
            'inn': data.get('inn', ''),
            'phone': data.get('phone', ''),
        }
        response = requests.post(gt_url, json=data, headers={'token': gt_token}, verify=False).json()
    else:
        response = {'error': 'method not allowed'}
    return jsonify(response)


@api.route('/add_lead', methods=['POST'])
@cross_origin()
def add_lead():
    data = request.get_json()
    if type(data) != list:
        data = [data, ]
    send_leads.delay(data)
    return jsonify(status='ok')
