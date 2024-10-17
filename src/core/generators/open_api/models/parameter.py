from typing import Dict, Any, Optional

from pydantic import BaseModel


class Parameter(BaseModel):
    """
    Model for the parameter object in the OpenAPI specification.
    """
    name: str
    in_: str
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    allowEmptyValue: Optional[bool] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None
    schema: Optional[Dict[str, Any]] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
