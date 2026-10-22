import base64

import requests
from loguru import logger
from requests.exceptions import HTTPError

from app.core.config import settings
from app.models.trading212_models import (
    LimitOrderPayload,
    MarketOrderPayload,
    StopOrderPayload,
    StopLimitOrderPayload,
)

CONTENT_TYPE = "application/json"


class Trading212Client:
    def __init__(self, dry_run: bool = False):
        self.api_key = settings.TRADING_212_API_KEY
        self.api_secret = settings.TRADING_212_API_SECRET
        self.username = settings.TRADING_212_API_KEY
        self.password = settings.TRADING_212_API_SECRET
        self.base_url = settings.trading_212_base_url
        self.dry_run = dry_run

        self.credentials_string = f"{self.api_key}:{self.api_secret}"
        self.encoded_credentials = base64.b64encode(
            self.credentials_string.encode("utf-8")
        ).decode("utf-8")
        self.auth_header = f"Basic {self.encoded_credentials}"

    def _is_live_order_blocked(self) -> bool:
        if self.dry_run:
            return True
        if settings.TRADING_212_ENVIRONMENT.strip().lower() == "live" and not settings.LIVE_TRADING_ENABLED:
            return True
        return False

    def get_account_summary(self):
        try:
            url = f"{self.base_url}/api/v0/equity/account/summary"
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

    def fetch_all_open_positions(self, query=None):
        try:
            url = f"{self.base_url}/api/v0/equity/positions"

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
            url = f"{self.base_url}/api/v0/equity/orders"

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
        if self._is_live_order_blocked():
            logger.warning(f"[DRY RUN] Skipping live limit order: {payload.model_dump()}")
            return {"status": "DRY_RUN", "simulated": True, "payload": payload.model_dump()}

        try:
            url = f"{self.base_url}/api/v0/equity/orders/limit"
            headers = {
                "Content-Type": CONTENT_TYPE,
                "Authorization": self.api_key,
            }
            auth = (self.username, self.password)

            response = requests.post(
                url, json=payload.model_dump(), headers=headers, auth=auth
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
        if self._is_live_order_blocked():
            logger.warning(f"[DRY RUN] Skipping live market order: {payload.model_dump()}")
            return {"status": "DRY_RUN", "simulated": True, "payload": payload.model_dump()}

        try:
            url = f"{self.base_url}/api/v0/equity/orders/market"
            headers = {
                "Content-Type": CONTENT_TYPE,
                "Authorization": self.api_key,
            }
            auth = (self.username, self.password)

            response = requests.post(
                url,
                json=payload.model_dump(),
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

    def place_stop_order(self, payload: StopOrderPayload):
        if self._is_live_order_blocked():
            logger.warning(f"[DRY RUN] Skipping live stop order: {payload.model_dump()}")
            return {"status": "DRY_RUN", "simulated": True, "payload": payload.model_dump()}

        try:
            url = f"{self.base_url}/api/v0/equity/orders/stop"
            headers = {
                "Content-Type": CONTENT_TYPE,
                "Authorization": self.api_key,
            }
            auth = (self.username, self.password)

            response = requests.post(
                url,
                json=payload.model_dump(),
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
        if self._is_live_order_blocked():
            logger.warning(f"[DRY RUN] Skipping live stop limit order: {payload.model_dump()}")
            return {"status": "DRY_RUN", "simulated": True, "payload": payload.model_dump()}

        try:
            url = f"{self.base_url}/api/v0/equity/orders/stop_limit"
            headers = {
                "Content-Type": CONTENT_TYPE,
                "Authorization": self.api_key,
            }
            auth = (self.username, self.password)

            response = requests.post(
                url,
                json=payload.model_dump(),
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
            url = f"{self.base_url}/api/v0/equity/orders/{id}"
            headers = {"Authorization": self.api_key}
            auth = (self.username, self.password)

            response = requests.delete(url, headers=headers, auth=auth)
            response.raise_for_status()

            if response.content:
                return response.json()
            return {"status": "CANCELLED", "id": id}
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
            url = f"{self.base_url}/api/v0/equity/orders/{id}"
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
            url = f"{self.base_url}/api/v0/equity/metadata/instruments"
            headers = {"Authorization": self.api_key}
            auth = (self.username, self.password)

            response = requests.get(url, headers=headers, auth=auth)

            data = response.json()
            return data
        except HTTPError as http_error:
            if response.status_code == 429:
                reset_timestamp = response.headers.get("x-ratelimit-reset")
                logger.error(f"Rate limit exceeded, limit resets at {reset_timestamp}")
                return None
            else:
                logger.error(f"HTTP error occurred: {http_error}")
        except Exception as err:
            logger.error(f"An unrelated error occurred: {err}")
            return None


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env.local")

    trading212_client = Trading212Client()

    summary = trading212_client.get_account_summary()

    print(summary)
