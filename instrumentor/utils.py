import os
import json


def get_spec_from_file(file_path: str) -> dict:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Spec file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
