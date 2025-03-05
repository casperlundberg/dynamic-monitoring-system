import json
import os

import jsonref

from typing import Dict, Any
import helper_functions as hf


def endpoint_generator(spec: Dict[str, Any]) -> None:
    paths = spec.get("paths")
    if paths is None:
        return

    for path, path_obj in paths.items():
        for method in path_obj.keys():
            f_name = hf.create_identifier(spec, path, method)
            generate_endpoint(f_name)

def generate_endpoint(f_name: str) -> None:
    endpoint_path = f"/{f_name.replace('_','/')}"
    endpoint_blueprint = f'blueprint_{f_name}'

######################
    endpoint = f"""from flask import Blueprint, Response, stream_with_context
from monitoring_backend.helper_functions import get_response

{endpoint_blueprint} = Blueprint('{endpoint_blueprint}', __name__)

@{endpoint_blueprint}.route('{endpoint_path}', methods=['GET'])
def {f_name}():
    response_data = get_response('{endpoint_path}')
    return Response(response_data, content_type='application/json')
"""
######################

    deploy_endpoint(endpoint, f_name)

def deploy_endpoint(endpoint: str, filename: str) -> None:
    target_folder = "generated_endpoints"
    target_filename = os.path.join(target_folder, f"{filename}.py")

    os.makedirs(target_folder, exist_ok=True)

    with open(target_filename, 'w') as f:
        f.write(endpoint)


with open('../dummy_api/dummy_api_spec.json', 'r') as file:
    test_spec = json.load(file)



# dereference json
dereferenced_spec = jsonref.replace_refs(test_spec)

# Run the endpoint generator
endpoint_generator(test_spec)