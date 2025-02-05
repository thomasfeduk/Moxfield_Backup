from datetime import datetime
from typing import List, Dict

from dtos.moxfield.moxfield_collections_search import CollectionSearchResponseDto
from debug import *

from includes.common import Collection
from clients.moxfield.moxfield_client import MoxfieldClient


def translate(personal_cards: Collection) -> List[Dict[str, any]]:
    """Define the mapping from DTO fields to CSV fields"""
    csv_rows = []
    die(personal_cards.json())
    for personal_card in personal_cards:
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


def binders():
    # binder_collection = client.get_trade_binders()
    cards = client.get_binder_cards()
    die(cards.json())
    csv_format = translate(cards)
    print(csv_format)
    die()
    pvdd(csv_format)
    for cardRoot in collection_search.data:
        print(cardRoot.card.name)

    die('end of runlocal')


if __name__ == "__main__":
    # if config.MoxFieldErrors.FRIENDLY_ERROR_MSG:
    #     os.environ['FRIENDLY_ERRORS'] = '1'

    client = MoxfieldClient()
    pvdd(client.get_csv())