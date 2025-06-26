from time import perf_counter
from pathlib import Path
from typing import Protocol, Iterable

from core.logger import log
from core.html_scraper import HtmlScraper
from core.json_scraper import JsonScraper
from core.storage import dump_to_csv, dump_to_sqlite
from core.models import CoinRecord

OUT_DIR = Path("output")
CSV_HTML = OUT_DIR / "coins_html.csv"
CSV_JSON = OUT_DIR / "coins_json.csv"
DB_FILE = OUT_DIR / "coins.db"

class DataScraper(Protocol):
    """Minimal typing protocol: any object exposing `.scrape() -> Iterable[CoinRecord]`."""

    def scrape(self) -> Iterable[CoinRecord]: ...


def benchmark(scraper: DataScraper, dst_csv: Path) -> tuple[int, float, float]:
    """
    Benchmark a scraper: fetch, persist, and compute throughput.

    Args:
        scraper: Instance implementing ``scrape()`` that yields ``CoinRecord`` objects.
        dst_csv: Destination CSV file for the scraped dataset.

    Returns:
        Tuple ``(rows, seconds, rows_per_second)``.
    """
    t0 = perf_counter()
    records = list(scraper.scrape())
    elapsed = perf_counter() - t0
    rps = len(records) / elapsed
    dump_to_csv(dst_csv, records)
    dump_to_sqlite(DB_FILE, records)
    return len(records), elapsed, rps


def main() -> None:
    """Run both scrapers, log metrics, and persist results to *output/*. """
    log.info("== HTML version ==")
    n, t, rps = benchmark(HtmlScraper(), CSV_HTML)
    log.info(f"Fetched {n} coins in {t:.2f}s  ➜  {rps:.2f} rows/s")

    log.info("== JSON version ==")
    n, t, rps = benchmark(JsonScraper(), CSV_JSON)
    log.info(f"Fetched {n} coins in {t:.2f}s  ➜  {rps:.2f} rows/s")


if __name__ == "__main__":
    main()
