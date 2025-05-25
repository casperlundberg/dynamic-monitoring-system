from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b5 = Blueprint('blueprint_post_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b5', __name__)

@blueprint_post_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b5.route('/post/temperature/b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b5', methods=['GET'])
def handle_post_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b5():
    response_data = get_response('post_temperature_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b5')
    return Response(response_data, content_type='application/json')
