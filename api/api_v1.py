from flask import Blueprint, request, jsonify
from .utils import make_request_to_1c

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify({'hello': 'bitch'})


@api.route('/ivr', methods=['GET', 'POST'])
def get_ivr_info():
    phone = request.args.get('phone')
    if phone:
        response = make_request_to_1c('ivr', {'phone': phone})
        return jsonify(response)
    return jsonify({'error': 'phone is undefined'})
