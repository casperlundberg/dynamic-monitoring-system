"""
Model for the server object in the OpenAPI specification.
uses pydantic for data validation
"""

from typing import Optional
from pydantic import BaseModel


# TODO: Add support for templating
class Server(BaseModel):
    """
    Model for the server object in the OpenAPI specification.
    """
    url: str
    description: Optional[str] = None
    variables: Optional[dict] = None
