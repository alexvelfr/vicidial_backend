from flask import Blueprint, request, jsonify
from .utils import make_request_to_1c

api = Blueprint('api', __name__)


@api.route('/ivr', methods=['GET', 'POST'])
def get_ivr_info():
    phone = request.args.get('phone')
    send_sms = bool(request.args.get('sendsms', False))
    if phone:
        response = make_request_to_1c('ivr', {'phone': phone, 'send_sms': send_sms})
        return jsonify(response)
    return jsonify({'error': 'phone is undefined'})
