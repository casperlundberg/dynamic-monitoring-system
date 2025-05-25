from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e86 = Blueprint('blueprint_post_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e86', __name__)

@blueprint_post_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e86.route('/post/energy/4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e86', methods=['GET'])
def handle_post_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e86():
    response_data = get_response('post_energy_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad5e86')
    return Response(response_data, content_type='application/json')
