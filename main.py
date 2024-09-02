import requests
from debug import *
import os
from includes.common import safe_filename
from datetime import datetime

class MoxfieldAPI:
    def __init__(self):
        self.username = 'Undefined'
        self._refresh_token_updated = False
        self._access_token = None

    def _update_refresh_token(self, token: str):
        with open('refresh_token.dat', 'w') as file:
            file.write(token)

    def refresh_token(self) -> str:
        with open('refresh_token.dat', 'r') as file:
            token = file.read()
        return token

    def get_access_token(self) -> str:
        if not self._refresh_token_updated:
            url = "https://api2.moxfield.com/v1/account/token/refresh"
            payload = json.dumps({
                "ignoreCookie": False
            })
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Content-Type': 'application/json',
                'x-moxfield-version': '2024.08.18.1',
                'Authorization': 'Bearer undefined',
                'Origin': 'https://www.moxfield.com',
                'Connection': 'keep-alive',
                'Referer': 'https://www.moxfield.com/',
                'Cookie': f'refresh_token={self.refresh_token()}; logged_in=true;',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site'
            }

            response = requests.post(url, headers=headers, data=payload)

            if response.status_code != 200:
                raise RuntimeError(f'Failed to obtain access token: Response {response.status_code}\n{response.text}')

            response_data = response.json()
            self._refresh_token_updated = True
            self._access_token = response_data["access_token"]
            print(f'Original refresh token: {self.refresh_token()}')
            self._update_refresh_token(response_data["refresh_token"])
            self.username = response_data["user_name"]
            print(f'New refresh token: {self.refresh_token()}')
        return self._access_token

    def get_binders(self) -> list:
        url = "https://api2.moxfield.com/v1/trade-binders"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.get_access_token()}',
            'Cookie': f'refresh_token={self.refresh_token()}; logged_in=true',
            'Origin': 'https://www.moxfield.com',
            'Referer': 'https://www.moxfield.com',
            'x-moxfield-version': '2024.08.18.1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'

        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(f'Failed to get collection: Response {response.status_code}\n{response.text}')
        data = json.loads(response.text)
        binders = [{"name": binder["name"], "publicId": binder["publicId"]} for binder in data]
        return binders

    def get_collection(self, binderId: str = ''):
        url = f"https://api2.moxfield.com/v1/trade-binders/{binderId}/search?pageNumber=1&pageSize=100&playStyle=paperDollars&sortType=cardName&sortDirection=ascending&q=+&setId=&deckId=&game=&condition=&rarity=&isAlter=&isProxy=&finish=&cardLanguageId=&priceMinimum=&priceMaximum="
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.get_access_token()}',
            'Cookie': f'refresh_token={self.refresh_token()}; logged_in=true',
            'Origin': 'https://www.moxfield.com',
            'Referer': 'https://www.moxfield.com',
            'x-moxfield-version': '2024.08.18.1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'

        }

        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        # Iterate through each element in the "data" list
        filenames = []
        for item in data.get("data", []):
            card_name = item.get("card", {}).get("name", "N/A")
            card_set = item.get("card", {}).get("set", "N/A")
            quantity = item.get("quantity", "N/A")
            finish = item.get("finish", "N/A")

            # print(f"Card Name: {card_name}")
            # print(f"Set: {card_set}")
            # print(f"Quantity: {quantity}")
            # print(f"Finish: {finish}")
            # print("-" * 30)

            filenames.append(f'{quantity} {card_name} ({card_set}) {finish}')

        return filenames

    def write_collection(self, binders: list):
        current_time = datetime.now().strftime("%Y-%m-%d %H;%M;%S")
        prefix = f'./MoxfieldBackups/{safe_filename(self.username)} - {current_time}'
        os.makedirs(f'{prefix}/collection')
        for binder in binders:
            os.makedirs(f'{prefix}/collection/{safe_filename(binder["name"])}')
            card_names = self.get_collection(binder["publicId"])
            for card in card_names:
                card_path = f'{prefix}/collection/{safe_filename(binder["name"])}'
                card_filename = f'{safe_filename(card)}.card'
                with open(f'{card_path}/{card_filename}', 'w') as file:
                    file.write('card')

