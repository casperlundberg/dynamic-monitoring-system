from typing import Optional

from pydantic import BaseModel


class Reference(BaseModel):
    """
    Model for the reference object in the OpenAPI specification.
    """
    ref: str
    summary: Optional[str] = None
    description: Optional[str] = None
