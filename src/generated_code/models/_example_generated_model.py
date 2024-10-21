from typing import List
from pydantic import BaseModel

from src.core.generators.open_api.models.misc import Tag


class Category:
    id: int
    name: str


class Pet(BaseModel):
    id: int
    category: Category
    name: str
    photo_urls: List[str]
    tags: List[Tag]
    status: str
