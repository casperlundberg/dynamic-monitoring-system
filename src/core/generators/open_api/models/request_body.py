from typing import Optional, Dict, Any

from pydantic import BaseModel


class RequestBody(BaseModel):
    """
    Model for the requestBody object in the OpenAPI specification.
    """
    description: Optional[str] = None
    content: Dict[str, Any]
    required: Optional[bool] = None
