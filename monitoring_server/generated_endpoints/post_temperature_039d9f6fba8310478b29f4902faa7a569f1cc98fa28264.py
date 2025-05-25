from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264 = Blueprint('blueprint_post_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264', __name__)

@blueprint_post_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264.route('/post/temperature/039d9f6fba8310478b29f4902faa7a569f1cc98fa28264', methods=['GET'])
def handle_post_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264():
    response_data = get_response('post_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264')
    return Response(response_data, content_type='application/json')
