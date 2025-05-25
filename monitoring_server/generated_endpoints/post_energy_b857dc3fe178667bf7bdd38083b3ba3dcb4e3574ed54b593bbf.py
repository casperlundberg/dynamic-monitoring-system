from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbf = Blueprint('blueprint_post_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbf', __name__)

@blueprint_post_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbf.route('/post/energy/b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbf', methods=['GET'])
def handle_post_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbf():
    response_data = get_response('post_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbf')
    return Response(response_data, content_type='application/json')
