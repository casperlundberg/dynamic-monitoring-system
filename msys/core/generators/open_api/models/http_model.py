from dataclasses import dataclass
from typing import Any


@dataclass
class HTTPModel:
    SERVER: str
    PATH: str
    path_params: dict
    request_args: dict
    url: str
    response: Any
    metrics: dict
    status_code: int
