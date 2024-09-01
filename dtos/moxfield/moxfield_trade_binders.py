from typing import List

from pydantic import RootModel

from dtos.base.data_types import StrPopulated, DatetimeIso8601
from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel


class CreatedByDto(MoxFieldBaseModel):
    userName: StrPopulated
    displayName: StrPopulated
    badges: List[StrPopulated]


class TradeBinderDto(MoxFieldBaseModel):
    id: StrPopulated
    name: StrPopulated
    description: StrPopulated
    publicId: StrPopulated
    visibility: StrPopulated
    createdAtUtc: DatetimeIso8601
    lastUpdatedAtUtc: DatetimeIso8601
    createdBy: CreatedByDto


class TradeBindersResponseDto(RootModel[List[TradeBinderDto]]):
    pass
