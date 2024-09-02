from dtos.moxfield.collections_search import CollectionSearchResponseDto
import os
import config
from debug import *

from clients.moxfield_client import MoxfieldClient


def binders():

    raw = client.get_trade_binders()
    pvdd(raw)
    for binder in bindersobj:
        pvdd(binder)

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
