from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbfa = Blueprint('blueprint_get_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbfa', __name__)

@blueprint_get_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbfa.route('/get/energy/b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbfa', methods=['GET'])
def handle_get_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbfa():
    response_data = get_response('get_energy_b857dc3fe178667bf7bdd38083b3ba3dcb4e3574ed54b593bbfa')
    return Response(response_data, content_type='application/json')
