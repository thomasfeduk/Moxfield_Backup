from includes.common import MyEnum


class FinishesEnum(str, MyEnum):
    FOIL = "foil"
    NONFOIL = "nonFoil"
    ETCHED = "etched"


class LegalitiesEnum(str, MyEnum):
    RESTRICTED = "restricted"
    LEGAL = "legal"
    NOT_LEGAL = "not_legal"


class CardCondition(MyEnum):
    MINT = 'mint'
    NEAR_MINT = 'nearMint'
    SLIGHTLY_PLAYED = 'slightlyPlayed'
    MODERATELY_PLAYED = 'moderatelyPlayed'
    HEAVILY_PLAYED = 'heavilyPlayed'
    DAMAGED = 'damaged'
