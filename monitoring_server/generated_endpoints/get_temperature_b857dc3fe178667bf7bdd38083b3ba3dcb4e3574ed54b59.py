from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b59 = Blueprint('blueprint_get_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b59', __name__)

@blueprint_get_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b59.route('/get/temperature/b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b59', methods=['GET'])
def handle_get_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b59():
    response_data = get_response('get_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b59')
    return Response(response_data, content_type='application/json')
