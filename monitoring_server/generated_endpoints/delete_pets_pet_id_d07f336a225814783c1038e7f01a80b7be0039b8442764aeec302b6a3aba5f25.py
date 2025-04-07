from flask import Blueprint, Response
from monitoring_server.Endpoint_generator.helper_functions import get_response

blueprint_delete_pets_pet_id_d07f336a225814783c1038e7f01a80b7be0039b8442764aeec302b6a3aba5f25 = Blueprint(
    'blueprint_delete_pets_pet_id_d07f336a225814783c1038e7f01a80b7be0039b8442764aeec302b6a3aba5f25',
    __name__)


@blueprint_delete_pets_pet_id_d07f336a225814783c1038e7f01a80b7be0039b8442764aeec302b6a3aba5f25.route(
    '/delete/pets/pet/id/d07f336a225814783c1038e7f01a80b7be0039b8442764aeec302b6a3aba5f25',
    methods=['GET'])
def handle_delete_pets_pet_id_d07f336a225814783c1038e7f01a80b7be0039b8442764aeec302b6a3aba5f25():
    response_data = get_response(
        '/delete/pets/pet/id/d07f336a225814783c1038e7f01a80b7be0039b8442764aeec302b6a3aba5f25')
    return Response(response_data, content_type='application/json')
