import base64
import requests
import time
from requests.exceptions import HTTPError
from loguru import logger

from app.core.config import settings
from app.models.trading212_models import (
    LimitOrderPayload,
    MarketOrderPayload,
    StopLimitOrderPayload,
)

CONTENT_TYPE = "application/json"


class Trading212Client:
    def __init__(self):
        self.api_key = settings.TRADING_212_API_KEY
        self.api_secret = settings.TRADING_212_API_SECRET
        self.username = settings.TRADING_212_API_KEY
        self.password = settings.TRADING_212_API_SECRET

        self.credentials_string = f"{self.api_key}:{self.api_secret}"
        self.encoded_credentials = base64.b64encode(
            self.credentials_string.encode("utf-8")
        ).decode("utf-8")
        self.auth_header = f"Basic {self.encoded_credentials}"

    def get_account_summary(self):
        try:
            url = "https://demo.trading212.com/api/v0/equity/account/summary"
            headers = {"Authorization": self.api_key}
            auth = (self.username, self.password)

            response = requests.get(url, headers=headers, auth=auth)

            data = response.json()
            return data
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def fetch_all_open_positions(self, query):
        try:
            url = "https://demo.trading212.com/api/v0/equity/positions"

            headers = {"Authorization": self.api_key}
            auth = (self.username, self.password)
            response = requests.get(url, headers=headers, params=query, auth=auth)

            data = response.json()
            return data
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def get_all_pending_orders(self):
        try:
            url = "https://demo.trading212.com/api/v0/equity/orders"

            headers = {"Authorization": self.api_key}
            auth = (self.username, self.password)
            response = requests.get(url, headers=headers, auth=auth)

            data = response.json()
            return data
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def place_limit_order(self, payload: LimitOrderPayload):
        try:
            url = "https://demo.trading212.com/api/v0/equity/orders/limit"
            headers = {
                "Content-Type": CONTENT_TYPE,
                "Authorization": self.api_key,
            }
            auth = (self.username, self.password)

            response = requests.post(
                url, json=payload.model_dump_json(), headers=headers, auth=auth
            )
            data = response.json()

            return data
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def place_market_order(self, payload: MarketOrderPayload):
        try:
            url = "https://demo.trading212.com/api/v0/equity/orders/market"
            headers = {
                "Content-Type": CONTENT_TYPE,
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
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def place_stop_order(self, payload: MarketOrderPayload):
        try:
            url = "https://demo.trading212.com/api/v0/equity/orders/stop"
            headers = {
                "Content-Type": CONTENT_TYPE,
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
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def place_stop_limit_order(self, payload: StopLimitOrderPayload):
        try:
            url = "https://demo.trading212.com/api/v0/equity/orders/stop_limit"
            headers = {
                "Content-Type": CONTENT_TYPE,
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
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def cancel_pending_order(self, id: int):
        try:
            url = "https://demo.trading212.com/api/v0/equity/orders/" + id
            headers = {"Authorization": self.api_key}
            auth = (self.username, self.password)

            response = requests.delete(url, headers=headers, auth=auth)

            data = response.json()
            return data
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def get_pending_order_by_id(self, id: int):
        try:
            url = "https://demo.trading212.com/api/v0/equity/orders/" + id
            headers = {"Authorization": self.api_key}
            auth = (self.username, self.password)

            response = requests.get(url, headers=headers, auth=auth)

            data = response.json()
            return data
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")

    def get_all_available_instruments(self):
        try:
            url = "https://demo.trading212.com/api/v0/equity/metadata/instruments"
            headers = {"Authorization": self.api_key}
            auth = (self.username, self.password)

            response = requests.get(url, headers=headers, auth=auth)

            data = response.json()
            return data
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env.local")

    trading212_client = Trading212Client()

    summary = trading212_client.get_account_summary()

    print(summary)
