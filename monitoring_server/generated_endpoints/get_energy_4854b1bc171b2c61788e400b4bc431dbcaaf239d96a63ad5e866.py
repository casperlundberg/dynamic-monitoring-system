from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e866 = Blueprint('blueprint_get_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e866', __name__)

@blueprint_get_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e866.route('/get/energy/4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e866', methods=['GET'])
def handle_get_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e866():
    response_data = get_response('get_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e866')
    return Response(response_data, content_type='application/json')
