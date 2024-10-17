"""
Parse the paths keyword found in the OpenAPI specification
"""
from typing import Dict, Any, List

from src.core.generators.open_api.models import Path


def parse_paths(paths: Dict[str, Dict[str, Any]]) -> List[Path]:
    """
    Parse the paths keyword in the OpenAPI specification.

    Args: paths: Paths in the OpenAPI specification.
    Returns: List of Path objects.
    """
    return [Path(path=path, methods=methods) for path, methods in
            paths.items()]


parse_paths(
    {
        "get": {
            "description": "Returns pets based on ID",
            "summary": "Find pets by ID",
            "operationId": "getPetsById",
            "responses": {
                "200": {
                    "description": "pet response",
                    "content": {
                        "*/*": {
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/Pet"
                                }
                            }
                        }
                    }
                },
                "default": {
                    "description": "error payload",
                    "content": {
                        "text/html": {
                            "schema": {
                                "$ref": "#/components/schemas/ErrorModel"
                            }
                        }
                    }
                }
            }
        },
        "parameters": [
            {
                "name": "id",
                "in": "path",
                "description": "ID of pet to use",
                "required": True,
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "style": "simple"
            }
        ]
    }
)
