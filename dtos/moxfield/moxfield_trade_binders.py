from __future__ import annotations
from typing import List
from dtos.moxfield.moxfield_basemodel import MyMoxRootModel
from dtos.moxfield.moxfield_shared import TradeBinderDetailedDto
from includes.common import RestrictedCollection


class TradeBindersResponseDto(MyMoxRootModel[List[TradeBinderDetailedDto]]):
    pass


class CollectionTradeBinders(RestrictedCollection[TradeBinderDetailedDto]):
    @property
    def expected_type(self) -> type:
        return TradeBinderDetailedDto
