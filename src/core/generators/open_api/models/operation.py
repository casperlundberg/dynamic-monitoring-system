# from typing import Optional, List, Union, Dict
#
# from pydantic import BaseModel
#
# from src.core.generators.open_api.models.request_body import RequestBody
# from src.core.generators.open_api.models.response import Response
# from src.core.generators.open_api.models.callback import Callback
# from src.core.generators.open_api.models.misc import ExternalDocs
# from src.core.generators.open_api.models.reference import Reference
# from src.core.generators.open_api.models.parameter import Parameter
# from src.core.generators.open_api.models.server import Server
#
#
# class Operation(BaseModel):
#     """
#     Model for the operation object in the OpenAPI specification.
#     """
#     tags: Optional[List[str]] = None
#     summary: Optional[str] = None
#     description: Optional[str] = None
#     externalDocs: Optional[ExternalDocs] = None
#     operationId: Optional[str] = None
#     parameters: Optional[List[Union[Parameter, Reference]]] = None
#     requestBody: Optional[Union[RequestBody, Reference]] = None
#     responses: Dict[str, Union[Response, Reference]]
#     callbacks: Optional[Dict[str, Union[Callback, Reference]]] = None
#     deprecated: Optional[bool] = None
#     security: Optional[List[Dict[str, List[str]]]] = None
#     servers: Optional[List[Server]] = None
