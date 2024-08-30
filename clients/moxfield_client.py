import requests
from cerberus import Validator
from includes.logger import get_logger
import config
from debug import *

from dtos.moxfield.moxfield_shared import UserBaseInfo
from dtos.moxfield.moxfield_auth import RefreshTokenResponseDto

log = get_logger()


class MoxfieldClient:
    def __init__(self, *, refresh_token: str):
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

    def _validate_token(self, refresh_token: str) -> str:
        schema = {'token': {'type': 'string', 'minlength': 1, 'regex': r'\S+'}}
        v = Validator(schema)
        if not v.validate({'token': refresh_token}):
            raise ValueError("refresh_token must be a non-empty string containing non-whitespace characters")
        return refresh_token

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
        pvdd(headers)

        response = requests.post(f"{config.MoxFieldAPI.BASE_URL}/{endpoint}", headers=headers, data=payload)
        response.raise_for_status()
        refresh_token_response = RefreshTokenResponseDto.load(response.json())
        pvdd(refresh_token_response)

        new_token = response.json().get('access_token')
        if new_token:
            self.api_key = new_token
            self.headers['Authorization'] = f'Bearer {self.api_key}'
            print("Token refreshed successfully.")
        else:
            print("Failed to refresh token.")
            raise Exception("Unable to refresh token; please reauthenticate.")
        return UserBaseInfo.load(refresh_token_response)

    # def get_collections(self) -> CollectionsSearchDTO:
    #     """Fetch collections data and return as DTO."""
    #     endpoint = "collections"
    #     response = self._make_request(endpoint)
    #     return CollectionsSearchDTO(**response)
    #
    # def _make_request(self, endpoint: str, method: str = 'GET', params=None, data=None, retry: bool = True):
    #     """Internal method to make HTTP requests with error handling for 401 Unauthorized."""
    #     url = f"{self.base_url}/{endpoint}"
    #     headers = {'Cookie': f'refresh_token={self.refresh_token}; logged_in=true;'}
    #     headers.update(self.headers)
    #
    #     try:
    #         response = requests.request(method, url, headers=self.headers, params=params, json=data)
    #         if response.status_code == 401 and retry:
    #             # Handle 401 Unauthorized: refresh the token and retry once
    #             self._refresh_token()
    #             return self._make_request(endpoint, method, params, data, retry=False)
    #         response.raise_for_status()
    #         # return response.json()
    #     except requests.exceptions.HTTPError as e:
    #         print(f"HTTP error occurred: {e} - Status Code: {response.status_code}")
    #         raise
    #     except requests.exceptions.RequestException as e:
    #         print(f"An error occurred: {e}")
    #         raise
