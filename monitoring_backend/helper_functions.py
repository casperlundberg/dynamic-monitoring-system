# @param enums: list
# @param inp: input to be tested
# @return: True if inp is in enums, False otherwise
import hashlib
import json
from typing import Dict, Any, Generator

import jsonref


def enum_tester(enums, inp):
    for enum in enums:
        if inp == enum:
            return True
    return False

def save_paths(paths: Dict[str, Any]) -> None:
    with open('paths.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, ensure_ascii=False, indent=4)

def load_paths() -> Dict[str, Any]:
    try:
        with open('paths.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: The file 'paths.json' was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: The file 'paths.json' contains invalid JSON.")
        return {}

def path_exists(paths: Dict[str, Any], path: str, i: int) -> bool:
    if path in paths:
        ids = paths[path]
        if i in ids:
            return True

    return False

def get_new_id(paths: Dict[str, Any], path: str) -> int:
    if path in paths:
        return max(paths[path]) + 1
    return 0

def prep_paths_for_save(paths: Dict[str, Any], path: str, i: int) -> Dict[str, Any]:
    if path in paths:
        paths[path].append(i)
    else:
        paths[path] = [i]
    return paths

def get_response(identifier: str):
    # get data from datasource (currently a file)
    with open('dummy_DB.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

        if identifier in db:
            def generate():
                for msg in db[identifier]:
                    yield json.dumps(msg) + '\n'

            return generate()
    return iter(["Could not find datasource"])


def generate_hash(spec: Dict[str, Any]) -> str:
    spec_str = json.dumps(spec, sort_keys=True)
    return hashlib.sha256(spec_str.encode('utf-8')).hexdigest()

def save_specification(spec: Dict[str, Any], filename: str = 'specifications.json') -> None:
    hash_value = generate_hash(spec)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            specs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        specs = {}

    specs[hash_value] = spec

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(specs, f, ensure_ascii=False, indent=4)

def load_specification(hash_value: str, filename: str = 'specifications.json') -> Dict[str, Any]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            specs = json.load(f)
        return specs.get(hash_value, {})
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: The file '{filename}' was not found or contains invalid JSON.")
        return {}

# def create_path_identifier(spec: Dict[str, Any], path: str) -> str:
#     hash_value = generate_hash(spec)
#     return f"{path.replace('{','').replace('}','')}_{hash_value}"

def create_identifier(spec: Dict[str, Any], path: str, method: str) -> str:
    hash_value = generate_hash(spec)
    return f"{method.lower()}{path.replace('/', '_').replace('{','').replace('}','')}_{hash_value}"[0:]

# with open('../docs/openapi.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Dereference the JSON document
# dereferenced_data = jsonref.replace_refs(data)
#
# # Print the dereferenced JSON document
# with open('../docs/deref_openapi.json', 'w', encoding='utf-8') as f:
#     json.dump(dereferenced_data, f, ensure_ascii=False, indent=4)