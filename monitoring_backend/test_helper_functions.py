import json
from helper_functions import save_specification, load_specification, create_endpoint_identifier, generate_hash


def test_save_and_load_specification():
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API",
            "version": "1.0.0"
        },
        "paths": {
            "/pet": {
                "get": {
                    "summary": "Get pet by ID",
                    "responses": {
                        "200": {
                            "description": "successful operation"
                        }
                    }
                }
            }
        }
    }

    # Save the specification
    save_specification(spec, 'test_specifications.json')

    # Generate hash for the specification
    hash_value = generate_hash(spec)

    # Load the specification
    loaded_spec = load_specification(hash_value, 'test_specifications.json')

    # Check if the loaded specification matches the original
    assert spec == loaded_spec, "Loaded specification does not match the original"

    print("Test save and load specification passed.")

def test_create_endpoint_identifier():
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API",
            "version": "1.0.0"
        },
        "paths": {
            "/pet": {
                "get": {
                    "summary": "Get pet by ID",
                    "responses": {
                        "200": {
                            "description": "successful operation"
                        }
                    }
                }
            }
        }
    }

    # Create an endpoint identifier
    endpoint_id = create_endpoint_identifier(spec, '/pet', 'get')

    # Generate hash for the specification
    hash_value = generate_hash(spec)

    # Check if the endpoint identifier is correct
    expected_endpoint_id = f'{hash_value}_/pet_get'
    assert endpoint_id == expected_endpoint_id, "Endpoint identifier does not match the expected value"

    print("Test create endpoint identifier passed.")

if __name__ == "__main__":
    test_save_and_load_specification()
    test_create_endpoint_identifier()