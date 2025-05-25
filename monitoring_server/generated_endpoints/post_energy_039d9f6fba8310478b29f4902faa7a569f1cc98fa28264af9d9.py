from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9 = Blueprint('blueprint_post_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9', __name__)

@blueprint_post_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9.route('/post/energy/039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9', methods=['GET'])
def handle_post_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9():
    response_data = get_response('post_energy_039d9f6fba8310478b29f4902faa7a569f1cc98fa28264af9d9')
    return Response(response_data, content_type='application/json')
