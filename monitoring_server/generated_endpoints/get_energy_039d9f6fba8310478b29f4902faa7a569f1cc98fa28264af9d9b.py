from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9b = Blueprint('blueprint_get_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9b', __name__)

@blueprint_get_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9b.route('/get/energy/039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9b', methods=['GET'])
def handle_get_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9b():
    response_data = get_response('get_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9b')
    return Response(response_data, content_type='application/json')
