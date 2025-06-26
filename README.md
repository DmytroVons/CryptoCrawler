# Crypto Crawler Challenge
---

## Project Structure

```
crypto_crawler/
├── core/                # isolated, single‑responsibility modules
│   ├── logger.py        # colourised, ISO‑8601 logging
│   ├── price_fetcher.py # provider‑agnostic REST fetcher (Phase 1)
│   ├── price_tracker.py # SMA window logic (Phase 1)
│   ├── html_scraper.py  # robust Next.js HTML → JSON parser (Phase 2)
│   ├── json_scraper.py  # direct CMC JSON endpoint scraper (Phase 2)
│   └── storage.py       # CSV + SQLite writers
├── main.py              # entry‑point for continuous 1 Hz price pulse
├── phase2.py            # grabs top‑100 coins & benchmarks scrapers
├── config.py            # tweakable constants (provider, SMA window,…)
├── output/              # CSV / SQLite artefacts (git‑ignored)
└── tests/               # pytest unit + integration suite
```

---

## Phase 1 – Price Pulse

| Feature                  | Detail                                                     |
| ------------------------ | ---------------------------------------------------------- |
| **Live price poller**    | 1 request ∕ sec to CoinGecko                               |
| **Exponential back‑off** | 1 → 2 → 4 → 8 s on network/5×× errors                      |
| **SMA(10)**              | simple moving average over last 10 ticks                   |
| **Graceful shutdown**    | `Ctrl‑C` ➜ finish in‑flight request ➜ log *Shutting down…* |

Run continuously:

```bash
python phase1.py
# [2025‑06‑26T15:01:24+00:00] BTC → USD: $106,995.17 | SMA(10): $107,012.11
```

---

## Phase 2 – CoinMarketCap Watchlist

1. **HTML Scraper** – parses `script#__NEXT_DATA__` JSON (works even when table rows are loaded via JS).
2. **JSON Scraper** – calls hidden CMC endpoint `https://api.coinmarketcap.com/data‑api/v3/cryptocurrency/listing`.
3. **Persistence** – writes identical rows to `out/coins_html.csv`, `out/coins_json.csv` and `out/coins.db`.
4. **Benchmark** – measures runtime & throughput and prints a comparison table.

Run once:

```bash
python phase2.py
# == HTML version ==  Fetched 100 coins in 1.08 s  ➜ 92 rows/s
# == JSON version == Fetched 100 coins in 0.24 s  ➜ 417 rows/s
```

---

## Installation

```bash
git clone https://github.com/DmytroVons/CryptoCrawler
cd CryptoCrawler
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the crawler

| Command                                       | Description                                          |
| --------------------------------------------- | ---------------------------------------------------- |
| `python phase1.py`                            | Continuous 1 Hz Bitcoin pulse with SMA(10)           |
| `python phase2.py`                            | Fetch + store top‑100 coins, then benchmark scrapers |

All CSV/DB files are written to the **`output/`** folder (git‑ignored).

---

## Running the test‑suite

```bash
pytest -q               # fast unit tests (no internet)
pytest -q -m integration # live API integration test
```

*Coverage* ≈ 95 % branch for Phase 1/2 modules (excluding I/O wrappers).

---

## Performance & Benchmarks

| Implementation | LoC | HTTP req. | Avg Runtime | Rows/s |
| -------------- | --- | --------- | ----------- | ------ |
| HTML scraper   | 115 | 5         | 1.05 s      | 95     |
| JSON scraper   | 78  | 1         | 0.24 s      | 417    |

---

## Extending / TODO

* **Async‑IO** version using `asyncio + aiohttp + websockets` for sub‑second latency.
* Automatic provider fallback (`CoinGecko → Binance → Coinbase`).
* Dockerfile + GitHub Actions CI (tests + flake8 + black).
* Configurable coin list (not just BTC / top‑100).
* Stream data to Kafka / TimescaleDB for long‑term storage.

---