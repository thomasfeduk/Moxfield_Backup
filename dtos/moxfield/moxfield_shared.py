from typing import List, Literal

from pydantic import StrictBool, StrictInt

from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel
from dtos.base.data_types import DatetimeIso8601, StrPopulated, DateYmd
from dtos.moxfield.moxfield_enums import FinishesEnum, LegalitiesEnum


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
    usd: float
    eur: float
    tix: float
    ck: float
    lastUpdatedAtUtc: DatetimeIso8601
    ck_buy: float
    csi: float
    csi_buy: float
    ct: float


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
    mana_cost: StrPopulated
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
    flavor_text: StrPopulated | None
    lang: StrPopulated
    latest: bool
    has_multiple_editions: bool
    has_arena_legal: bool
    prices: CardPricesDto
    artist: StrPopulated
    promo_types: List[StrPopulated]
    cardHoarderUrl: StrPopulated | None
    cardKingdomUrl: StrPopulated | None
    cardMarketUrl: StrPopulated | None
    tcgPlayerUrl: StrPopulated | None
    isArenaLegal: bool
    released_at: DateYmd
    edhrec_rank: int | None
    cardmarket_id: int | None
    mtgo_id: int | None
    tcgplayer_id: int | None
    cardkingdom_id: int | None
    reprint: bool
    set_type: StrPopulated
    coolStuffIncUrl: StrPopulated | None
    acorn: bool
    image_seq: int
    cardTraderUrl: StrPopulated | None
    content_warning: bool
    isToken: bool
    defaultFinish: FinishesEnum
