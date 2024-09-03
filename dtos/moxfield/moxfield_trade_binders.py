from __future__ import annotations
from typing import List
from dtos.moxfield.moxfield_basemodel import MyMoxRootModel
from dtos.moxfield.moxfield_shared import TradeBinderDto
from includes.common import RestrictedCollection


class TradeBindersResponseDto(MyMoxRootModel[List[TradeBinderDto]]):
    pass


class TradeBindersCollection(RestrictedCollection[TradeBinderDto]):
    @property
    def expected_type(self) -> type:
        return TradeBinderDto
