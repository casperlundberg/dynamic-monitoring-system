import jsonref

from typing import Dict, Any


def clean_dereference(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean dereference the OpenAPI spec by removing JSON references.
    This function is used to clean the dereferenced spec before storing it.

    Args:
        spec (Dict[str, Any]): The OpenAPI spec to clean.

    Returns:
        Dict[str, Any]: The cleaned OpenAPI spec without JSON references.
    """
    if not spec:
        return {}

    # Use jsonref to dereference the spec
    deref = jsonref.JsonRef.replace_refs(spec)

    # Strip JSON references
    cleaned_spec = strip_jsonref(deref)

    return cleaned_spec


def strip_jsonref(obj):
    if isinstance(obj, dict):
        return {k: strip_jsonref(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [strip_jsonref(i) for i in obj]
    elif isinstance(obj, jsonref.JsonRef):
        return strip_jsonref(obj.__subject__)
    return obj
