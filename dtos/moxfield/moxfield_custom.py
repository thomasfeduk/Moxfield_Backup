from datetime import datetime
from typing import List, Dict

from dtos.base.data_types import StrPopulated
from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel
from dtos.moxfield.moxfield_shared import TradeBinderSimpledDto, CollectionPersonalCards


class CollectionSet(MoxFieldBaseModel):
    username: StrPopulated
    binder: TradeBinderSimpledDto = None
    personalCards: CollectionPersonalCards

    def get_tokens(self) -> CollectionPersonalCards:
        return CollectionPersonalCards([])

    def get_csv_format(self, headers: bool = True, *, tokens: bool = True) -> List[Dict[str, str | int]]:
        csv_rows = []
        for personal_card in self.personalCards:
            csv_row = {
                "Count": 1,
                "Tradelist Count": 0,
                "Name": personal_card.card.name,
                "Edition": personal_card.card.set_name,
                "Condition": "NM",
                "Language": personal_card.card.lang,
                "Foil": "Yes" if personal_card.isFoil else "No",
                "Tags": "",
                "Last Modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Collector Number": personal_card.card.cn,
                "Alter": "No",
                "Proxy": "No",
                "Purchase Price": 0
            }
            csv_rows.append(csv_row)
        return csv_rows

    def get_bulk_format(self, tokens: bool = False):
        ...

    def write_csv(self, file: str, *, tokens: bool = True, overwrite: bool = False):
        ...
