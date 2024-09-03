from enum import Enum


class FinishesEnum(str, Enum):
    foil = "foil"
    nonFoil = "nonFoil"
    etched = "etched"


class LegalitiesEnum(str, Enum):
    restricted = "restricted"
    legal = "legal"
    not_legal = "not_legal"

