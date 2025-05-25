from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1c = Blueprint('blueprint_post_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1c', __name__)

@blueprint_post_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1c.route('/post/energy/e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1c', methods=['GET'])
def handle_post_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1c():
    response_data = get_response('post_energy_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e75e1c')
    return Response(response_data, content_type='application/json')
