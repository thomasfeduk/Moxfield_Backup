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


class TradeBindersCollection(RestrictedCollection):
    def __init__(self, items: list = None):
        super().__init__(items)

    @property
    def expected_type(self):
        return TradeBinderDto

    def __iter__(self) -> Iterator[TradeBinderDto]:
        return super().__iter__()

    def __add__(self, value: TradeBinderDto | RestrictedCollection) -> TradeBindersCollection:
        return super().__add__(value)

    # Override get item so we can typehint the explicit type
    def __getitem__(self, index) -> TradeBinderDto:
        return super().__getitem__(index)

    # Override get item so we can typehint the explicit type
    def __next__(self) -> TradeBinderDto:
        return super().__next__()
