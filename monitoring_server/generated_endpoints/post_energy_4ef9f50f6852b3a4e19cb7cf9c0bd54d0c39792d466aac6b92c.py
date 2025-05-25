from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c = Blueprint('blueprint_post_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c', __name__)

@blueprint_post_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c.route('/post/energy/4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c', methods=['GET'])
def handle_post_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c():
    response_data = get_response('post_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c')
    return Response(response_data, content_type='application/json')
