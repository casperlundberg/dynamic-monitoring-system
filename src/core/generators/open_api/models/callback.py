# from typing import Dict, Union
#
# from pydantic import BaseModel
#
# from src.core.generators.open_api.models.path import Path, Reference
#
#
# class Callback(BaseModel):
#     """
#     Model for the callback object in the OpenAPI specification.
#     """
#     expression: str
#     callback: Dict[str, Union[Path, Reference]]
from typing import Dict, Union

from pydantic import BaseModel


def get_callback():
    """
    Get the callback object in the OpenAPI specification.
    """
    from src.core.generators.open_api.models.path import Path
    from src.core.generators.open_api.models.reference import Reference

    class Callback(BaseModel):
        """
        Model for the callback object in the OpenAPI specification.
        """
        expression: str
        callback: Dict[str, Union[Path, Reference]]

    return Callback
