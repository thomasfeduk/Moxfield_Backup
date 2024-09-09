from typing import Dict, List

from includes.csv_writer import CSVWriter
from debug import *
from clients.moxfield.moxfield_api import MoxfieldApi
from dtos.moxfield.moxfield_custom import CollectionSet
from dtos.moxfield.moxfield_shared import CollectionPersonalCards


class MoxfieldClient:
    def __init__(self):
        """Inits the API client which immediately attempts to confirm a valid auth token"""
        with open('refresh_token.dat', 'r') as token_file:
            token = token_file.read()

        self._api = MoxfieldApi(refresh_token=token)

    def get_csv(self) -> List[Dict[str, str | int]]:

        # example_header = ["Count", "Tradelist Count", "Name", "Edition", "Condition",
        #                   "Language", "Foil", "Tags", "Last Modified", "Collector Number",
        #                   "Alter", "Proxy", "Purchase Price"]
        #
        # example_rows_list = [
        #     [1, 0, "Card A", "Set A", "NM", "EN", "No", "", "2024-09-08 10:00:00", "123", "No", "No", 10],
        #     [2, 1, "Card B", "Set B", "EX", "FR", "Yes", "", "2024-09-08 11:00:00", "456", "No", "No", 20]
        # ]
        #
        # csv_writer = CSVWriter(filename='example_output.csv', header=example_header)
        #
        # # Write rows using a list of lists
        # result_list = csv_writer.add_row_via_list(example_rows_list)

        collection = self.get_collection()
        csv = collection.get_csv_format(headers=False)
        pvdd(csv)
        pvdd(collection)
        return
        # pvdd(collection_pcards)

    def get_collection(self, binder_id: str = None) -> CollectionSet:
        collection_pcards = self._api.get_binder_cards()
        return CollectionSet(username="sadsds", personalCards=collection_pcards)

