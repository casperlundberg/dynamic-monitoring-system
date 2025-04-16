from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7 = Blueprint('blueprint_post_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7', __name__)

@blueprint_post_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7.route('/post/temperature/edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7', methods=['GET'])
def handle_post_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7():
    response_data = get_response('post_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7')
    return Response(response_data, content_type='application/json')
