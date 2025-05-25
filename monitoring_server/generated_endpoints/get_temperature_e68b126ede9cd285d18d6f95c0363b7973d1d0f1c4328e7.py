from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e7 = Blueprint('blueprint_get_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e7', __name__)

@blueprint_get_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e7.route('/get/temperature/e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e7', methods=['GET'])
def handle_get_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e7():
    response_data = get_response('get_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e7')
    return Response(response_data, content_type='application/json')
