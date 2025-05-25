from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

blueprint_post_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63a = Blueprint('blueprint_post_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63a', __name__)

@blueprint_post_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63a.route('/post/temperature/4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63a', methods=['GET'])
def handle_post_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63a():
    response_data = get_response('post_temperature_4854b1bc171b2c61788e400b4bc431dbcaaf239d96a63a')
    return Response(response_data, content_type='application/json')
