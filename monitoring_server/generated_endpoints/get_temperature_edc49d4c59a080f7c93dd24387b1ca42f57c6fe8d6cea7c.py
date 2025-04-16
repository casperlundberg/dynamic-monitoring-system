from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c = Blueprint('blueprint_get_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c', __name__)

@blueprint_get_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c.route('/get/temperature/edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c', methods=['GET'])
def handle_get_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c():
    response_data = get_response('get_temperature_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c')
    return Response(response_data, content_type='application/json')
