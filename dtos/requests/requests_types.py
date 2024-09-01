from typing import Any, Dict

from pydantic import RootModel
from dtos.base.basemodel import MyBaseModel

class JsonDto(RootModel[Dict[Any, Any]]):
    pass
