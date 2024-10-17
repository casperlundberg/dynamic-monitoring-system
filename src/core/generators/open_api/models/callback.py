from typing import Dict, Union

from pydantic import BaseModel

from src.core.generators.open_api.models.path import Path, Reference


class Callback(BaseModel):
    """
    Model for the callback object in the OpenAPI specification.
    """
    expression: str
    callback: Dict[str, Union[Path, Reference]]
