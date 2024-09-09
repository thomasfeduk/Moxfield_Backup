from __future__ import annotations

from typing import List

from pydantic import StrictBool, BaseModel, StrictInt, StrictStr, StrictFloat

from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel
from dtos.base.data_types import DatetimeIso8601, StrPopulated, DateYmd
from dtos.moxfield.moxfield_enums import FinishesEnum, LegalitiesEnum
from includes.common import RestrictedCollection


class UserBaseInfo(MoxFieldBaseModel):
    user_name: StrPopulated
    email_address: StrPopulated
    is_email_confirmed: StrictBool
    permissions: List[StrPopulated]
    user_id: StrPopulated
    mature_content_pref: StrPopulated
    date_of_birth: DateYmd


class LegalitiesDto(MoxFieldBaseModel):
    standard: LegalitiesEnum
    future: LegalitiesEnum
    historic: LegalitiesEnum
    timeless: LegalitiesEnum
    gladiator: LegalitiesEnum
    pioneer: LegalitiesEnum
    explorer: LegalitiesEnum
    modern: LegalitiesEnum
    legacy: LegalitiesEnum
    pauper: LegalitiesEnum
    vintage: LegalitiesEnum
    penny: LegalitiesEnum
    commander: LegalitiesEnum
    oathbreaker: LegalitiesEnum
    standardbrawl: LegalitiesEnum
    brawl: LegalitiesEnum
    alchemy: LegalitiesEnum
    paupercommander: LegalitiesEnum
    duel: LegalitiesEnum
    oldschool: LegalitiesEnum
    premodern: LegalitiesEnum
    predh: LegalitiesEnum


class CardPricesDto(MoxFieldBaseModel):
    usd: float = None
    eur: float = None
    tix: float = None
    ck: float = None
    lastUpdatedAtUtc: DatetimeIso8601 = None
    ck_buy: float = None
    csi: float = None
    csi_buy: float = None
    ct: float = None


class CardDto(MoxFieldBaseModel):
    id: StrPopulated
    uniqueCardId: StrPopulated
    scryfall_id: StrPopulated
    set: StrPopulated
    set_name: StrPopulated
    name: StrPopulated
    cn: StrPopulated
    layout: StrPopulated
    cmc: float
    type: StrPopulated
    type_line: StrPopulated
    oracle_text: StrPopulated
    mana_cost: str
    colors: List[StrPopulated]
    color_indicator: List[StrPopulated]
    color_identity: List[StrPopulated]
    legalities: LegalitiesDto
    frame: StrPopulated
    reserved: bool
    digital: bool
    foil: bool
    nonfoil: bool
    etched: bool
    glossy: bool
    rarity: StrPopulated
    border_color: StrPopulated
    colorshifted: bool
    flavor_text: str = None
    lang: StrPopulated
    latest: bool
    has_multiple_editions: bool
    has_arena_legal: bool
    prices: CardPricesDto
    artist: StrPopulated
    promo_types: List[StrPopulated]
    cardHoarderUrl: StrPopulated = None
    cardKingdomUrl: StrPopulated = None
    cardMarketUrl: StrPopulated = None
    tcgPlayerUrl: StrPopulated = None
    isArenaLegal: bool
    released_at: DateYmd
    edhrec_rank: int = None
    cardmarket_id: int = None
    mtgo_id: int = None
    tcgplayer_id: int = None
    cardkingdom_id: int = None
    reprint: bool
    set_type: StrPopulated
    coolStuffIncUrl: StrPopulated = None
    acorn: bool
    image_seq: int
    cardTraderUrl: StrPopulated = None
    content_warning: bool
    isToken: bool
    defaultFinish: FinishesEnum


class TradeBinderSimpledDto(MoxFieldBaseModel):
    id: StrPopulated
    name: StrPopulated
    publicId: StrPopulated


class TradeBinderDetailedDto(MoxFieldBaseModel):
    id: StrPopulated
    name: StrPopulated
    description: str
    publicId: StrPopulated
    visibility: StrPopulated
    createdAtUtc: DatetimeIso8601
    lastUpdatedAtUtc: DatetimeIso8601
    createdBy: CreatedByDto


class PersonalCardDto(MoxFieldBaseModel):
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
    tradeBinder: TradeBinderSimpledDto = None
    card: CardDto


class CollectionPersonalCards(RestrictedCollection[PersonalCardDto]):
    @property
    def expected_type(self) -> type:
        return PersonalCardDto


class CreatedByDto(MoxFieldBaseModel):
    userName: StrPopulated
    displayName: StrPopulated
    badges: List[StrPopulated]


class CsvFormatCollectionDTO(MoxFieldBaseModel):
    Count: StrictInt
    Tradelist_Count: StrictInt
    Name: StrictStr
    Edition: StrictStr
    Condition: StrictStr
    Language: StrictStr
    Foil: StrictStr
    Tags: StrictStr
    Last_Modified: StrictStr
    Collector_Number: StrictStr
    Alter: StrictStr
    Proxy: StrictStr
    Purchase_Price: StrictFloat
