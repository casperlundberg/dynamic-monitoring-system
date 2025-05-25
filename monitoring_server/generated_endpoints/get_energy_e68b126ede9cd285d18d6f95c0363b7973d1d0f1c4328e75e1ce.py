from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1ce = Blueprint('blueprint_get_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1ce', __name__)

@blueprint_get_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1ce.route('/get/energy/e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1ce', methods=['GET'])
def handle_get_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1ce():
    response_data = get_response('get_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1ce')
    return Response(response_data, content_type='application/json')
