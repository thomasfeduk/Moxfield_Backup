from datetime import datetime
from typing import List, Dict

from dtos.moxfield.moxfield_collections_search import CollectionSearchResponseDto
import os
import config
from debug import *

from clients.moxfield_client import MoxfieldClient
from dtos.moxfield.moxfield_shared import CardDto


def translate(card_dtos: List[CardDto]) -> List[Dict[str, any]]:
    # Define the mapping from DTO fields to CSV fields
    csv_rows = []
    for card in card_dtos:
        csv_row = {
            "Count": 1,  # Assuming 1 by default, modify as needed
            "Tradelist Count": 0,  # Assuming 0 by default, modify as needed
            "Name": card.name,
            "Edition": card.set_name,
            "Condition": "NM",  # Defaulting to Near Mint (NM), modify as needed
            "Language": card.lang,
            "Foil": "Yes" if card.foil else "No",
            "Tags": "",  # No tag data in DTO, add logic if available
            "Last Modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Default to current time
            "Collector Number": card.cn,
            "Alter": "No",  # Defaulting to No, modify as needed
            "Proxy": "No",  # Defaulting to No, modify as needed
            "Purchase Price": "",  # No purchase price in DTO, add logic if available
        }
        csv_rows.append(csv_row)

    return csv_rows

def binders():

    # binder_collection = client.get_trade_binders()
    collection_search = client.collections_search()
    # pvdd(len(collection_search.data))

    # pvdd([item for item in collection_search.data])

    csv_format = translate([item.card for item in collection_search.data])
    pvdd(csv_format)
    for cardRoot in collection_search.data:
        print(cardRoot.card.name)

    die('end of runlocal')


if __name__ == "__main__":
    # if config.MoxFieldErrors.FRIENDLY_ERROR_MSG:
    #     os.environ['FRIENDLY_ERRORS'] = '1'


    with open('refresh_token.dat', 'r') as token_file:
        token = token_file.read()

    client = MoxfieldClient(refresh_token=token)


    binders()



    # moxfield_api = MoxfieldAPI()
    # binders = moxfield_api.get_binders()
    # moxfield_api.write_collection(binders)
    # moxfield_api.get_collection()




    die('runlocalpy')


    with open('dto_refs/collection/response CollectionsSearch.json', 'r') as fidle:
        data = file.read()

    response = CollectionSearchResponseDto.load(data)
    print(response.totalPages)
