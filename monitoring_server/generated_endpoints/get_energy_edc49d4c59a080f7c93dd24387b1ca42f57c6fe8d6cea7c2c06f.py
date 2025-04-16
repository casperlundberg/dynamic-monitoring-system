from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_energy_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c2c06f = Blueprint('blueprint_get_energy_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c2c06f', __name__)

@blueprint_get_energy_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c2c06f.route('/get/energy/edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c2c06f', methods=['GET'])
def handle_get_energy_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c2c06f():
    response_data = get_response('get_energy_edc49d4c59a080f7c93dd24387b1ca42f57c6fe8d6cea7c2c06f')
    return Response(response_data, content_type='application/json')
