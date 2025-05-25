from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c2 = Blueprint('blueprint_get_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c2', __name__)

@blueprint_get_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c2.route('/get/energy/4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c2', methods=['GET'])
def handle_get_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c2():
    response_data = get_response('get_energy_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6b92c2')
    return Response(response_data, content_type='application/json')
