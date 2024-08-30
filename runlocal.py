from dtos.moxfield.collections_search import CollectionSearchResponseDto
import os
import config
from debug import *

from clients.moxfield_client import MoxfieldClient

def auth():
    with open('refresh_token.dat', 'r') as token_file:
        token = token_file.read()
    client = MoxfieldClient(refresh_token=token)
    client.authenticate()
    die('sadsaasd')


if __name__ == "__main__":
    # if config.MoxFieldErrors.FRIENDLY_ERROR_MSG:
    #     os.environ['FRIENDLY_ERRORS'] = '1'

    # moxfield_api = MoxfieldAPI()
    # binders = moxfield_api.get_binders()
    # moxfield_api.write_collection(binders)
    # moxfield_api.get_collection()

    auth()



    die('runlocalpy')


    with open('dto_refs/collection/response CollectionsSearch.json', 'r') as fidle:
        data = file.read()

    response = CollectionSearchResponseDto.load(data)
    print(response.totalPages)
