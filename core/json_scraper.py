from time import perf_counter
from typing import Iterable
from requests import get
from urllib.parse import urlencode
from core.logger import log
from core.models import CoinRecord
from core.scraper import DataScraper

BASE = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing"


class JsonScraper(DataScraper):
    """
    Fast scraper that fetches cryptocurrency data from an unauthenticated JSON API endpoint.

    Attributes:
        limit (int): Number of cryptocurrencies to fetch, sorted by market cap.
    """

    def __init__(self, limit: int = 100):
        """
        Initializes the JSON scraper.

        Args:
            limit (int): Max number of coins to fetch. Defaults to 100.
        """
        self.limit = limit

    def scrape(self) -> Iterable[CoinRecord]:
        """
        Fetches and parses cryptocurrency data into CoinRecord instances.

        Returns:
            Iterable[CoinRecord]: Generator of parsed coin records.
        """
        params = {
            "start": 1,
            "limit": self.limit,
            "sortBy": "market_cap",
            "sortType": "desc",
            "convert": "USD",
            "cryptoType": "all",
            "tagType": "all",
        }
        url = f"{BASE}?{urlencode(params)}"
        t0 = perf_counter()
        data = get(url, timeout=10).json()["data"]["cryptoCurrencyList"]
        log.debug(f"GET {url} ({perf_counter()-t0:.2f}s)")
        return (
            CoinRecord(
                c["cmcRank"],
                c["name"],
                c["symbol"],
                c["quotes"][0]["price"],
                c["quotes"][0]["percentChange24h"],
                c["quotes"][0]["marketCap"],
            )
            for c in data
        )
