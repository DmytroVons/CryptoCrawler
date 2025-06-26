from collections import deque
from statistics import mean


class PriceTracker:
    """
    Tracks a sliding window of recent prices and computes SMA (Simple Moving Average).
    """

    def __init__(self, window_size: int):
        """
        Initializes the tracker with a fixed window size.

        Args:
            window_size (int): Number of most recent prices to consider for SMA.
        """
        self.prices = deque(maxlen=window_size)

    def add_price(self, price: float) -> None:
        """
        Adds a new price to the tracker.

        Args:
            price (float): The new BTC price.
        """
        self.prices.append(price)

    def get_sma(self) -> float | None:
        """
        Computes the simple moving average of the current window.

        Returns:
            float | None: The average price if window is full, otherwise None.
        """
        if len(self.prices) < self.prices.maxlen:
            return None
        return round(mean(self.prices), 2)
