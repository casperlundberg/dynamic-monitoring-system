from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e = Blueprint('blueprint_post_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e', __name__)

@blueprint_post_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e.route('/post/temperature/e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e', methods=['GET'])
def handle_post_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e():
    response_data = get_response('post_temperature_e68b126ede9cd285d18d6f95c0363b7973d1d0f1c4328e')
    return Response(response_data, content_type='application/json')
