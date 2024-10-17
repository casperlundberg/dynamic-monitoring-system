from typing import List, Dict, Any

from src.core.generators.open_api.models.misc import Tag, License, Contact, \
    Info, ExternalDocs


def parse_tags(tags: List[Dict[str, Any]]) -> List[Tag]:
    """
    Parse the tags keyword in the OpenAPI specification.

    Args: tags: List of tags in the OpenAPI specification.
    Returns: List of Tag objects.
    """
    return [Tag(**tag) for tag in tags]


def parse_license(_license: Dict[str, Any]) -> License:
    """
    Parse the license keyword in the OpenAPI specification.

    Args: license: License in the OpenAPI specification.
    Returns: License object.
    """
    return License(**_license)


def parse_contact(contact: Dict[str, Any]) -> Contact:
    """
    Parse the contact keyword in the OpenAPI specification.

    Args: contact: Contact in the OpenAPI specification.
    Returns: Contact object.
    """
    return Contact(**contact)


def parse_external_docs(external_docs: Dict[str, Any]) -> ExternalDocs:
    """
    Parse the externalDocs keyword in the OpenAPI specification.

    Args: external_docs: ExternalDocs in the OpenAPI specification.
    Returns: ExternalDocs object.
    """
    return ExternalDocs(**external_docs)


def parse_info(info: Dict[str, Any]) -> Info:
    """
    Parse the info keyword in the OpenAPI specification.

    Args: info: Info in the OpenAPI specification.
    Returns: Info object.
    """
    return Info(**info)
