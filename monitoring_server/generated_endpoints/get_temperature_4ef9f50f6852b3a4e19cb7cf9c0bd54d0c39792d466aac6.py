from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6 = Blueprint('blueprint_get_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6', __name__)

@blueprint_get_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6.route('/get/temperature/4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6', methods=['GET'])
def handle_get_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6():
    response_data = get_response('get_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac6')
    return Response(response_data, content_type='application/json')
