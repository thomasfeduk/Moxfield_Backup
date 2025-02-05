import csv
from datetime import datetime
from typing import List, Dict

from debug import *
from dtos.base.data_types import StrPopulated
from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel
from dtos.moxfield.moxfield_shared import TradeBinderSimpledDto, CollectionPersonalCards, CsvFormatCollectionDTO
from includes.csv_writer import CSVWriter


class CsvSupport:
    def write_csv(self, file: str, csv_data: List[List[str | int | float]], *, overwrite: bool = False):
        mode = 'w' if overwrite else 'a'
        with open(file, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)

class CollectionSet(MoxFieldBaseModel, CsvSupport):
    username: StrPopulated
    binder: TradeBinderSimpledDto = None
    personalCards: CollectionPersonalCards

    def get_tokens(self) -> CollectionPersonalCards:
        return CollectionPersonalCards([])

    def get_csv_format(self, headers: bool = True, *, tokens: bool = True) -> List[List[str | int | float]]:
        csv_rows = []
        if headers:
            csv_rows.append(list(CsvFormatCollectionDTO.model_fields.keys()))
        for personal_card in self.personalCards:
            csv_row = CsvFormatCollectionDTO(
                Count=1,
                Tradelist_Count=0,
                Name=personal_card.card.name,
                Edition=personal_card.card.set_name,
                Condition="NM",
                Language=personal_card.card.lang,
                Foil="Yes" if personal_card.isFoil else "No",
                Tags="",
                Last_Modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                Collector_Number=personal_card.card.cn,
                Alter="No",
                Proxy="No",
                Purchase_Price=0.0
            )
            csv_rows.append(csv_row.to_list())
        pvdd(csv_rows)
        return csv_rows

    def get_bulk_format(self, tokens: bool = False):
        ...

    def write_csv(self, file: str, *, tokens: bool = True, overwrite: bool = False):
        ...
