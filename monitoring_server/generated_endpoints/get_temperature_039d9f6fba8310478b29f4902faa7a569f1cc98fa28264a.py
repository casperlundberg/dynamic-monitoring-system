from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264a = Blueprint('blueprint_get_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264a', __name__)

@blueprint_get_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264a.route('/get/temperature/039d9f6fba8310478b29f4902faa7a569f1cc98fa28264a', methods=['GET'])
def handle_get_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264a():
    response_data = get_response('get_temperature_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264a')
    return Response(response_data, content_type='application/json')
