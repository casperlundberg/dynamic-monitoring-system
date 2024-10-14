from typing import Optional
from pydantic import BaseModel


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
