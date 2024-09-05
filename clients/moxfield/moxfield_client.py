from typing import Dict, List

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


        pvdd(collection_pcards)

    def get_collection(self) -> CollectionSet:
        collection_pcards = self._api.get_binder_cards()
        return CollectionSet()

