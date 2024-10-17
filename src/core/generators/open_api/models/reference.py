from pydantic import BaseModel


class Reference(BaseModel):
    """
    Model for the reference object in the OpenAPI specification.
    """
    ref: str
