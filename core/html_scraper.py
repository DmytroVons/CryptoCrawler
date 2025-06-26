from json import loads
from typing import Iterable
from collections.abc import Mapping, Sequence
from bs4 import BeautifulSoup
from requests import Session
from core.logger import log
from core.models import CoinRecord
from core.scraper import DataScraper

BASE_URL = "https://coinmarketcap.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def _find_listing(node: object) -> list[dict] | None:
    """
    Recursively searches for the 'cryptoCurrencyList' key in a nested JSON-like structure.

    Args:
        node (object): A JSON node (dict or list) to search within.

    Returns:
        list[dict] | None: The value of 'cryptoCurrencyList' if found, otherwise None.
    """
    if isinstance(node, Mapping):
        if "cryptoCurrencyList" in node:
            return node["cryptoCurrencyList"]
        for v in node.values():
            res = _find_listing(v)
            if res:
                return res
    elif isinstance(node, Sequence) and not isinstance(node, (str, bytes)):
        for item in node:
            res = _find_listing(item)
            if res:
                return res
    return None


class HtmlScraper(DataScraper):
    """
    Scraper that extracts cryptocurrency data from CoinMarketCap HTML using a Next.js JSON blob.

    This parser avoids JavaScript execution and WebDriver by parsing the embedded
    JSON inside <script id="__NEXT_DATA__">.

    Attributes:
        pages (int): Number of paginated listing pages to scrape.
    """

    def __init__(self, pages: int = 5):
        """
        Initializes the HTML scraper.

        Args:
            pages (int): Number of CoinMarketCap pages to scrape. Defaults to 5.
        """
        self.pages = pages

    def scrape(self) -> Iterable[CoinRecord]:
        """
        Scrapes cryptocurrency data from HTML and parses it into CoinRecord instances.

        Returns:
            Iterable[CoinRecord]: List of parsed coin records.
        """
        records: list[CoinRecord] = []
        session = Session()
        session.headers.update(HEADERS)

        for page in range(1, self.pages + 1):
            url = f"{BASE_URL}/?page={page}"
            html = session.get(url, timeout=10).text
            soup = BeautifulSoup(html, "lxml")
            tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
            if not (tag and tag.string):
                log.warning("script#__NEXT_DATA__ not found")
                continue

            try:
                payload = loads(tag.string)
                listing = _find_listing(payload)
                if not listing:
                    raise KeyError("cryptoCurrencyList not found")
            except Exception as exc:
                log.error(f"Cannot parse __NEXT_DATA__: {exc}")
                continue

            for c in listing:
                try:
                    quotes = c["quotes"][0]
                    records.append(
                        CoinRecord(
                            rank=c["cmcRank"],
                            name=c["name"],
                            symbol=c["symbol"],
                            price_usd=quotes["price"],
                            change_24h=quotes["percentChange24h"],
                            market_cap=quotes["marketCap"],
                        )
                    )
                except (KeyError, TypeError):
                    continue

        return records