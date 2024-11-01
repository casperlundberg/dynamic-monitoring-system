from dataclasses import dataclass
from typing import *


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Pet:
    id: int
    category: Category
    name: str
    photo_urls: List[str]
    status: str


@dataclass
class Items:
    type: str
    enum: List[str]


@dataclass
class Hourly:
    name: str
    in_: str
    schema: Items
