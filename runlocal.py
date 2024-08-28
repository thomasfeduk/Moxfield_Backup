from dtos.moxfield.collections_search import CollectionSearchResponseDto
import os
import config

if __name__ == "__main__":
    if config.MoxFieldErrors.FRIENDLY_ERROR_MSG:
        os.environ['FRIENDLY_ERRORS'] = '1'

    # moxfield_api = MoxfieldAPI()
    # binders = moxfield_api.get_binders()
    # moxfield_api.write_collection(binders)
    # moxfield_api.get_collection()

    with open('dto_refs/collection/response CollectionsSearch.json', 'r') as file:
        data = file.read()

    response = CollectionSearchResponseDto.load(data)
    print(response.totalPages)
