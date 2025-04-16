from typing import Dict, Any
import os
import json


# get openapi spec from folder defined in config, namely PATH_TO_OPENAPI_SPEC
def get_spec_from_folder(folder_path: str) -> Dict[str, Any]:
    """
    Load OpenAPI spec from a folder and return it as a dictionary.
    """
    spec_files = [f for f in os.listdir(folder_path) if
                  f.endswith('.yaml') or f.endswith('.json')]
    if not spec_files:
        raise FileNotFoundError(
            "No OpenAPI spec files found in the specified folder.")

    # Assuming we want to load the first spec file found
    spec_file_path = os.path.join(folder_path, spec_files[0])

    with open(spec_file_path, 'r') as file:
        if spec_file_path.endswith('.yaml'):
            import yaml
            spec = yaml.safe_load(file)
        else:
            spec = json.load(file)

    return spec
