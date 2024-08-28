from typing import List
from dtos.base.data_types import StrPopulated, DatetimeIso8601
from dtos.moxfield.moxfield_shared import FinishesEnum, CardDto
from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel


class TradeBinderDto(MoxFieldBaseModel):
    id: StrPopulated
    publicId: StrPopulated
    name: StrPopulated


class DataDto(MoxFieldBaseModel):
    id: StrPopulated
    quantity: int
    condition: StrPopulated
    game: StrPopulated
    finish: FinishesEnum
    isFoil: bool
    isAlter: bool
    isProxy: bool
    isPrefPrinting: bool
    createdAtUtc: DatetimeIso8601
    lastUpdatedAtUtc: DatetimeIso8601
    rarity: StrPopulated
    tradeBinder: TradeBinderDto
    card: CardDto


class CollectionSearchResponseDto(MoxFieldBaseModel):
    totalOverall: int
    totalCommon: int
    totalUncommon: int
    totalRare: int
    totalMythic: int
    isEmpty: bool
    pageNumber: int
    pageSize: int
    totalResults: int
    totalPages: int
    data: List[DataDto]
