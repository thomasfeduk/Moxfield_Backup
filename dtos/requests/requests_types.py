from typing import Any, Dict

from pydantic import RootModel
from dtos.base.basemodel import MyRootModel


class JsonDto(MyRootModel[Dict[Any, Any]]):
    pass