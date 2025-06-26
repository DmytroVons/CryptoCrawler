from requests import get, RequestException
from config import API_URL, QUERY_PARAMS
from core.logger import log


class PriceFetcher:
    """
    Fetches the latest BTC price and timestamp from the external API.
    Retries are tracked for failure handling.
    """

    def __init__(self):
        """
        Initializes the fetcher with retry count set to zero.
        """
        self.retries = 0

    def fetch_price(self):
        """
        Retrieves the current BTC price and its last update timestamp.

        Returns:
            tuple[float, int]: Price in USD and UNIX timestamp.

        Raises:
            RequestException: On HTTP/network errors.
            KeyError: If expected data keys are missing.
        """
        try:
            response = get(API_URL, params=QUERY_PARAMS, timeout=5)
            response.raise_for_status()
            data = response.json()
            price = data["bitcoin"]["usd"]
            timestamp = data["bitcoin"]["last_updated_at"]
            self.retries = 0
            return price, timestamp
        except (RequestException, KeyError) as e:
            log.warning(f"Fetch failed: {e}")
            self.retries += 1
            raise
