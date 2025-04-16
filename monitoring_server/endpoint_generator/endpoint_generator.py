import os

from typing import Dict, Any

import packages.identifier.identfier as identifier


def endpoint_generator(spec: Dict[str, Any]) -> None:
    paths = spec.get("paths")
    if paths is None:
        return

    for path, path_obj in paths.items():
        for method in path_obj.keys():
            f_name = identifier.create_identifier(spec, path, method)
            generate_endpoint(f_name)


def generate_endpoint(f_name: str) -> None:
    endpoint_path = f"/{f_name.replace('_', '/')}"
    endpoint_blueprint = f'blueprint_{f_name}'

    ######################
    endpoint = f"""from flask import Blueprint, Response, stream_with_context
from monitoring_server.helper_functions import get_response

{endpoint_blueprint} = Blueprint('{endpoint_blueprint}', __name__)

@{endpoint_blueprint}.route('{endpoint_path}', methods=['GET'])
def handle_{f_name}():
    response_data = get_response('{f_name}')
    return Response(response_data, content_type='application/json')
"""
    ######################

    deploy_endpoint(endpoint, f_name)


def deploy_endpoint(endpoint: str, filename: str) -> None:
    target_folder = os.path.join(os.path.dirname(__file__),
                                 '../generated_endpoints')
    abs_folder = os.path.abspath(target_folder)
    print(f"[endpoint_generator] Writing to: {abs_folder}")  # 👈 NEW

    target_filename = os.path.join(target_folder, f"{filename}.py")
    os.makedirs(target_folder, exist_ok=True)

    with open(target_filename, 'w') as f:
        f.write(endpoint)
