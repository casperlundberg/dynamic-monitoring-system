"""
Model that describe a single path in the OpenAPI specification.
Must utilize sub-models to describe the path.
"""

from typing import List, Optional, Union

from pydantic import BaseModel

from src.core.generators.open_api.models.operation import Operation
from src.core.generators.open_api.models.parameter import Parameter
from src.core.generators.open_api.models.reference import Reference
from src.core.generators.open_api.models.server import Server


class Path(BaseModel):
    """
    Model for the path object in the OpenAPI specification.
    """
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    trace: Optional[Operation] = None
    servers: Optional[List[Server]] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None
