from clients.moxfield_api import MoxfieldApi


class MoxfieldClient:
    def __init__(self):
        """Inits the API client which immediately attempts to confirm a valid auth token"""
        with open('refresh_token.dat', 'r') as token_file:
            token = token_file.read()
        self._api = MoxfieldApi(refresh_token=token)

