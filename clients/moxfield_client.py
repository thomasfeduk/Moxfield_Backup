import config
from dtos.moxfield.moxfield_collections_search import CollectionSearchResponseDto
from includes.types import JSONType
from clients.base_client import Requests
from cerberus import Validator
from includes.logger import get_logger
from debug import *

from dtos.moxfield.moxfield_shared import UserBaseInfo
from dtos.moxfield.moxfield_auth import RefreshTokenResponseDto
from dtos.moxfield.moxfield_trade_binders import TradeBindersResponseDto, TradeBindersCollection, TradeBinderDto

log = get_logger()


class AuthFailure(Exception):
    pass


class MoxfieldClient:
    def __init__(self, *, refresh_token: str):
        self._access_token = None
        self._refresh_token = self._validate_token(refresh_token)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'x-moxfield-version': '2024.08.18.1',
            'Origin': 'https://www.moxfield.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.moxfield.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }

        # Auto authenticate to grab a fresh refresh token when initlizing the client
        self.authenticate()

    def authenticate(self) -> UserBaseInfo:
        """Refresh the authentication token and update user info."""
        endpoint = "/v1/account/token/refresh"
        headers = {}
        headers.update({'Authorization': 'Bearer undefined'})
        headers.update({'Cookie': f'refresh_token={self._refresh_token}; logged_in=true;'})
        headers.update(self.headers)
        payload = json.dumps({
            "ignoreCookie": False
        })

        response = Requests.post(f"{config.MoxFieldAPI.BASE_URL}/{endpoint}", headers=headers, data=payload)

        # If we get an invalid token error, prompt the user to enter a fresh token error
        # Yes moxfield uses 400 instead of 401 for failed token auth
        if response.status_code == 400 and "Invalid refresh token" in response.text:
            pvdd("Your token expired enter a new one")

        # Throw exception if not 2xx, 400 is already handled above
        response.raise_for_status()
        refresh_token_response = RefreshTokenResponseDto.load(response.json())

        # Update/store the refresh and access tokens
        self._access_token = refresh_token_response.access_token
        self._update_stored_refresh_token(refresh_token_response)
        return UserBaseInfo.load(refresh_token_response)

    def get_trade_binders(self) -> TradeBindersCollection:
        """Fetch collections data and return as DTO."""
        endpoint = "/v1/trade-binders"
        response = self._make_request(endpoint)
        # Confirm response validity since response is a simple list of TradeBinders
        TradeBindersResponseDto.load(response)
        return TradeBindersCollection([TradeBinderDto.load(item) for item in response])

    def collections_search(self) -> CollectionSearchResponseDto:
        """Fetch collections data and return as DTO."""
        endpoint = "/v1/collections/search"
        params = {
            'q': '',
            'setId': '',
            'deckId': '',
            'rarity': '',
            'condition': '',
            'game': '',
            'cardLanguageId': '',
            'finish': '',
            'isAlter': '',
            'isProxy': '',
            'tradeBinderId': '',
            'playStyle': 'paperDollars',
            'priceMinimum': '',
            'priceMaximum': '',
            'pageNumber': '1',
            'pageSize': '50',
            'sortType': 'cardName',
            'sortDirection': 'ascending'
        }
        response = self._make_request(endpoint, params=params)
        pvddfile('swamp',response)
        return CollectionSearchResponseDto.load(response)

    def _make_request(self, endpoint: str, method: str = 'GET', params=None, data=None) -> JSONType:
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Cookie': f'refresh_token={self._refresh_token}; logged_in=true'
        }
        headers.update(self.headers)
        try:
            response = Requests.request(method, f"{config.MoxFieldAPI.BASE_URL}{endpoint}",
                                        headers=headers, params=params, json=data)
            response.raise_for_status()
        except Requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e} - Status Code: {response.status_code}")
            raise
        except Requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            raise
        return response.json()

    @classmethod
    def _update_stored_refresh_token(cls, refresh_token_response: RefreshTokenResponseDto):
        if not isinstance(refresh_token_response, RefreshTokenResponseDto):
            raise ValueError("refresh_token must be an instance of type RefreshTokenResponseDto")

        with open(f'refresh_token.dat', 'w') as file:
            file.write(refresh_token_response.refresh_token)
            log.info('Updated refresh token.')

    @classmethod
    def _validate_token(cls, refresh_token: str) -> str:
        schema = {'token': {'type': 'string', 'minlength': 1, 'regex': r'\S+'}}
        v = Validator(schema)
        if not v.validate({'token': refresh_token}):
            raise ValueError("refresh_token must be a non-empty string containing non-whitespace characters")
        return refresh_token
