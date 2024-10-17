from typing import List, Optional, Union, Dict

from pydantic import BaseModel

from src.core.generators.open_api.models.callback import get_callback
from src.core.generators.open_api.models.misc import ExternalDocs
from src.core.generators.open_api.models.parameter import Parameter
from src.core.generators.open_api.models.reference import Reference
from src.core.generators.open_api.models.request_body import RequestBody
from src.core.generators.open_api.models.response import Response
from src.core.generators.open_api.models.server import Server


class Operation(BaseModel):
    """
    Model for the operation object in the OpenAPI specification.
    """
    tags: Optional[List[str]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocs] = None
    operationId: Optional[str] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None
    requestBody: Optional[Union[RequestBody, Reference]] = None
    responses: Dict[str, Union[Response, Reference]]
    callbacks: Optional[Dict[str, Union[get_callback(), Reference]]] = None
    deprecated: Optional[bool] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    servers: Optional[List[Server]] = None


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
