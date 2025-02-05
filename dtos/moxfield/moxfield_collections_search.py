from typing import List
from dtos.base.data_types import StrPopulated
from dtos.moxfield.moxfield_shared import PersonalCardDto
from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel


class TradeBinderDto(MoxFieldBaseModel):
    id: StrPopulated
    publicId: StrPopulated
    name: StrPopulated


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
    data: List[PersonalCardDto]
