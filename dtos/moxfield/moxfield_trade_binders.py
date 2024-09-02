from __future__ import annotations
from typing import List, Iterator
from dtos.base.data_types import StrPopulated, DatetimeIso8601
from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel, MyMoxRootModel
from includes.common import RestrictedCollection


class CreatedByDto(MoxFieldBaseModel):
    userName: StrPopulated
    displayName: StrPopulated
    badges: List[StrPopulated]


class TradeBinderDto(MoxFieldBaseModel):
    id: StrPopulated
    name: StrPopulated
    description: str
    publicId: StrPopulated
    visibility: StrPopulated
    createdAtUtc: DatetimeIso8601
    lastUpdatedAtUtc: DatetimeIso8601
    createdBy: CreatedByDto


class TradeBindersResponseDto(MyMoxRootModel[List[TradeBinderDto]]):
    pass


class TradeBindersCollection(RestrictedCollection[TradeBinderDto]):
    @property
    def expected_type(self) -> type:
        return TradeBinderDto
