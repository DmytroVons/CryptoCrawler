from time import sleep
from datetime import datetime
from core.price_fetcher import PriceFetcher
from core.price_tracker import PriceTracker
from core.shutdown_handler import GracefulShutdown
from core.logger import log
from config import FETCH_INTERVAL, SMA_WINDOW_SIZE, MAX_RETRIES


def format_line(price: float, timestamp: int, sma: float | None) -> str:
    """
    Format the output line with price, timestamp, and optional SMA.

    Args:
        price: The current BTC price in USD.
        timestamp: UNIX timestamp of the current price.
        sma: Simple Moving Average of the last N prices, or None.

    Returns:
        A formatted string with timestamp, BTC price, and optionally the SMA.
    """
    ts = datetime.fromtimestamp(timestamp).isoformat()
    line = f"[{ts}] BTC → USD: ${price:,.2f}"
    if sma is not None:
        line += f" | SMA({SMA_WINDOW_SIZE}): ${sma:,.2f}"
    return line


def main() -> None:
    """
    Main polling loop to fetch BTC price every interval, track SMA,
    and handle retries and graceful shutdown.

    Uses:
        - PriceFetcher to retrieve live BTC price from API.
        - PriceTracker to maintain moving average.
        - GracefulShutdown to listen for termination signals.
        - Logs formatted output to console or file.
    """
    fetcher = PriceFetcher()
    tracker = PriceTracker(SMA_WINDOW_SIZE)
    shutdown_handler = GracefulShutdown()

    retry_delay = FETCH_INTERVAL

    while not shutdown_handler.shutdown:
        try:
            price, ts = fetcher.fetch_price()
            tracker.add_price(price)
            sma = tracker.get_sma()
            log.info(format_line(price, ts, sma))
            retry_delay = FETCH_INTERVAL
        except Exception:
            if fetcher.retries >= MAX_RETRIES:
                log.error(f"Exceeded {MAX_RETRIES} retries. Continuing polling.")
                fetcher.retries = 0
                retry_delay = FETCH_INTERVAL
            else:
                retry_delay *= 2
        sleep(retry_delay)


if __name__ == "__main__":
    main()
