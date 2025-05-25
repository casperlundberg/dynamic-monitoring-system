from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_get_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad = Blueprint('blueprint_get_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad', __name__)

@blueprint_get_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad.route('/get/temperature/4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad', methods=['GET'])
def handle_get_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad():
    response_data = get_response('get_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63ad')
    return Response(response_data, content_type='application/json')
