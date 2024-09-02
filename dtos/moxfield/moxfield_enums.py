from enum import Enum


class FinishesEnum(str, Enum):
    value1 = "foil"
    value2 = "nonFoil"
    value3 = "etched"


class LegalitiesEnum(str, Enum):
    value1 = "legal"
    value2 = "not_legal"
