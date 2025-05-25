from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac = Blueprint('blueprint_post_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac', __name__)

@blueprint_post_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac.route('/post/temperature/4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac', methods=['GET'])
def handle_post_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac():
    response_data = get_response('post_temperature_4ef9f50f6852b3a4e19cb7cf9c0bd54d0c39792d466aac')
    return Response(response_data, content_type='application/json')
