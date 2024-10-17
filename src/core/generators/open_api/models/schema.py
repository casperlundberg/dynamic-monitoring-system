# from typing import Optional, Dict, Any, List
#
# from pydantic import BaseModel
#
# from src.core.generators.open_api.models import ExternalDocs
#
#
# class Discriminator(BaseModel):
#     """
#     Model for the discriminator object in the OpenAPI specification.
#     """
#     propertyName: str
#     mapping: Optional[Dict[str, str]] = None
#
#
# class XML(BaseModel):
#     """
#     Model for the xml object in the OpenAPI specification.
#     """
#     name: Optional[str] = None
#     namespace: Optional[str] = None
#     prefix: Optional[str] = None
#     attribute: Optional[bool] = None
#     wrapped: Optional[bool] = None
#
#
# class Schema(BaseModel):
#     """
#     Model for the schema object in the OpenAPI specification.
#     """
#     # type: str
#     # required: Optional[List[str]] = None
#     # properties: Optional[Dict[str, Any]] = None
#
#     discriminator: Optional[Discriminator] = None
#     xml: Optional[XML] = None
#     externalDocs: Optional[ExternalDocs] = None
#
#     # allOf: Optional[List[Dict[str, Any]]] = None
#     # oneOf: Optional[List[Dict[str, Any]]] = None
#     # anyOf: Optional[List[Dict[str, Any]]] = None
#     # not_: Optional[Dict[str, Any]] = None
#     # items: Optional[Dict[str, Any]] = None
