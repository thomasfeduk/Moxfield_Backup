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


class LanguageEnum(MyEnum):
    ENGLISH = "LD58x"
    SPANISH = "YxlpG"
    FRENCH = "kAVXO"
    GERMAN = "YnWyB"
    ITALIAN = "EJ5yA"
    PORTUGUESE = "YdK6v"
    JAPANESE = "EP6jq"
    KOREAN = "LmyKq"
    RUSSIAN = "k71wl"
    SIMPLIFIED_CHINESE = "YlgbQ"
    TRADITIONAL_CHINESE = "LVN4j"
    HEBREW = "Y2P4X"
    LATIN = "ErnAR"
    ANCIENT_GREEK = "E53lZ"
    ARABIC = "YoDab"
    SANSKRIT = "Yjn7Z"
    PHYREXIAN = "E6QRq"
