"""
Unit-тести HtmlScraper / JsonScraper з моками + live-integration.

Патч-шляхи:
  • HtmlScraper  → core.html_scraper.Session.get
  • JsonScraper  → core.json_scraper.get          (імпортовано як 'get')
"""

from unittest.mock import Mock
import json
import pytest
import requests

from core.html_scraper import HtmlScraper
from core.json_scraper import JsonScraper
from core.models import CoinRecord


def make_next_data_html(listing: list[dict]) -> str:
    payload = {
        "props": {
            "initialState": {
                "cryptocurrency": {
                    "listingLatest": {"data": {"cryptoCurrencyList": listing}}
                }
            }
        }
    }
    return (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(payload) +
        "</script></body></html>"
    )


SAMPLE_LISTING = [
    {
        "cmcRank": 2,
        "name": "Bitcoin",
        "symbol": "BTC",
        "quotes": [
            {
                "price": 70123.45,
                "percentChange24h": 1.23,
                "marketCap": 1_234_567_890.0,
            }
        ],
    }
]

SAMPLE_HTML = make_next_data_html(SAMPLE_LISTING)


@pytest.fixture
def mock_html(monkeypatch):
    """Patch Session.get so HtmlScraper receives SAMPLE_HTML."""
    def fake_get(self, url, timeout):
        return Mock(text=SAMPLE_HTML)

    monkeypatch.setattr("core.html_scraper.Session.get", fake_get)


def test_html_scraper_parses_single_page(mock_html):
    records = list(HtmlScraper(pages=1).scrape())

    assert len(records) == 1
    rec: CoinRecord = records[0]
    assert rec.rank == 2
    assert rec.name == "Bitcoin"
    assert rec.symbol == "BTC"
    assert rec.price_usd == 70123.45
    assert rec.change_24h == 1.23
    assert rec.market_cap == 1_234_567_890.0


@pytest.fixture
def mock_json(monkeypatch):
    """Patch 'get' imported inside JsonScraper."""
    sample_json = {"data": {"cryptoCurrencyList": SAMPLE_LISTING}}

    def fake_get(url, timeout):
        resp = Mock()
        resp.json = lambda: sample_json
        return resp

    monkeypatch.setattr("core.json_scraper.get", fake_get)


def test_json_scraper_parses_single_row(mock_json):
    records = list(JsonScraper(limit=1).scrape())

    assert len(records) == 1
    rec = records[0]
    assert rec.rank == 2
    assert rec.name == "Bitcoin"
    assert rec.symbol == "BTC"
    assert rec.price_usd == 70123.45
    assert rec.change_24h == 1.23
    assert rec.market_cap == 1_234_567_890.0


@pytest.mark.integration
def test_json_scraper_live():
    """Calls real CoinMarketCap JSON endpoint (slow, network-dependent)."""
    try:
        records = list(JsonScraper(limit=100).scrape())
    except requests.RequestException:
        pytest.skip("Network unreachable — інтеграційний тест пропущено")

    assert len(records) == 100
    assert all(r.price_usd > 0 for r in records)
