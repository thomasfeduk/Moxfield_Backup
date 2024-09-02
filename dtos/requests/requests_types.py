from typing import Any, Dict, List, Union

from pydantic import RootModel
from dtos.base.basemodel import MyRootModel


class JsonDto(MyRootModel[Union[Dict[str, Any], List[Any], str, int, float, bool, None]]):
    """Used for requests response.json() return types"""
    pass
