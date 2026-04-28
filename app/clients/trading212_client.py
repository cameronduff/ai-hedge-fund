import base64
import requests

from app.core.config import settings
from app.models.trading212_models import LimitOrderPayload, MarketOrderPayload


class Trading212Client:
    api_key = settings.TRADING_212_API_KEY
    api_secret = settings.TRADING_212_API_SECRET
    username = settings.TRADING_212_USERNAME
    password = settings.TRADING_212_PASSWORD

    credentials_string = f"{api_key}:{api_secret}"
    encoded_credentials = base64.b64encode(credentials_string.encode("utf-8")).decode(
        "utf-8"
    )
    auth_header = f"Basic {encoded_credentials}"

    def fetch_all_open_positions(self, query):
        url = "https://demo.trading212.com/api/v0/equity/positions"

        headers = {"Authorization": self.api_key}
        auth = (self.username, self.password)
        response = requests.get(url, headers=headers, params=query, auth=auth)

        data = response.json()
        return data

    def get_all_pending_orders(self):
        url = "https://demo.trading212.com/api/v0/equity/orders"

        headers = {"Authorization": self.api_key}
        auth = (self.username, self.password)
        response = requests.get(url, headers=headers, auth=auth)

        data = response.json()
        return data

    def place_limit_order(self, payload: LimitOrderPayload):
        url = "https://demo.trading212.com/api/v0/equity/orders/limit"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }
        auth = (self.username, self.password)

        response = requests.post(
            url, json=payload.model_dump_json(), headers=headers, auth=auth
        )
        data = response.json()

        return data

    def place_market_order(self, payload: MarketOrderPayload):
        url = "https://demo.trading212.com/api/v0/equity/orders/market"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

        auth = (self.username, self.password)

        response = requests.post(
            url,
            json=payload.model_dump_json(),
            headers=headers,
            auth=auth,
        )

        data = response.json()
        return data
