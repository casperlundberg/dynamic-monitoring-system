from typing import Optional, Dict, Any, Union

from pydantic import BaseModel

from src.core.generators.open_api.models.reference import Reference


class Response(BaseModel):
    """
    Model for the response object in the OpenAPI specification.
    """
    description: str
    headers: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    links: Optional[Dict[str, Any]] = None


class Responses(BaseModel):
    """
    Model for the responses object in the OpenAPI specification.
    """
    default: Optional[Response] = None
    http_status_codes: Optional[Dict[str, Union[Response, Reference]]]
