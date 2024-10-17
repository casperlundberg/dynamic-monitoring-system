from typing import Optional, Any, Dict, Union
from pydantic import BaseModel

from src.core.generators.open_api.models.reference import Reference


class ExternalDocs(BaseModel):
    """
    Model for the externalDocs object in the OpenAPI specification.
    """
    description: Optional[str] = None
    url: str


class Tag(BaseModel):
    """
    Model for the tag object in the OpenAPI specification.
    """
    name: str
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocs] = None


class Contact(BaseModel):
    """
    Model for the contact object in the OpenAPI specification.
    """
    name: Optional[str] = None
    email: Optional[str] = None


class License(BaseModel):
    """
    Model for the license object in the OpenAPI specification.
    """
    name: str
    url: Optional[str] = None


class Info(BaseModel):
    """
    Model for the info object in the OpenAPI specification.
    """
    title: str
    description: Optional[str] = None
    termsOfService: Optional[str] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None
    version: str


class Example(BaseModel):
    """
    Model for the example object in the OpenAPI specification.
    """
    summary: Optional[str] = None
    description: Optional[str] = None
    value: Any
    externalValue: Optional[str] = None


class Encoding(BaseModel):
    """
    Model for the encoding object in the OpenAPI specification.
    """
    contentType: Optional[str] = None
    headers: Optional[Dict[str, Any]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None

    # class Config:
    #     arbitrary_types_allowed = True


class MediaType(BaseModel):
    """
    Model for the mediaType object in the OpenAPI specification.
    """
    schema: Optional[Union[Reference, Dict[str, Any]]] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Reference, Example]]] = None
    encoding: Optional[Dict[str, Encoding]] = None


class Link(BaseModel):
    """
    Model for the link object in the OpenAPI specification.
    """
    operationRef: Optional[str] = None
    operationId: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    requestBody: Optional[Any] = None
    description: Optional[str] = None
    server: Optional[Dict[str, Any]] = None


class Header(BaseModel):
    """
    Model for the header object in the OpenAPI specification.
    """
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    allowEmptyValue: Optional[bool] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None
    schema: Optional[Union[Reference, Dict[str, Any]]] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Reference, Example]]] = None
    content: Optional[Dict[str, MediaType]] = None
