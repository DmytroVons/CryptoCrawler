from unittest.mock import Mock
from pytest import fixture, raises
import requests

from core.price_fetcher import PriceFetcher

@fixture
def fetcher():
    return PriceFetcher()


def test_price_fetcher_success(monkeypatch, fetcher):
    sample_json = {
        "bitcoin": {"usd": 12345.67, "last_updated_at": 1_725_000_000}
    }

    def _fake_get(url, params, timeout):
        resp = Mock(status_code=200)
        resp.json = lambda: sample_json
        resp.raise_for_status = lambda: None
        return resp

    monkeypatch.setattr("core.price_fetcher.get", _fake_get)

    price, ts = fetcher.fetch_price()

    assert price == 12345.67
    assert ts == 1_725_000_000
    assert fetcher.retries == 0


def test_price_fetcher_failure_increments_retries(monkeypatch, fetcher):
    def _fake_get(url, params, timeout):
        resp = Mock(status_code=500)
        resp.raise_for_status = lambda: (_ for _ in ()).throw(
            requests.HTTPError(response=resp)
        )
        return resp

    monkeypatch.setattr("core.price_fetcher.get", _fake_get)

    with raises(requests.HTTPError):
        fetcher.fetch_price()

    assert fetcher.retries == 1