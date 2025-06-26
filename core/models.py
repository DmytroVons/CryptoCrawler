from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class CoinRecord:
    """
    Represents a single cryptocurrency record parsed from a data source.

    Attributes:
        rank (int): Position in the coin ranking list.
        name (str): Full name of the coin (e.g., "Bitcoin").
        symbol (str): Ticker symbol (e.g., "BTC").
        price_usd (float): Current price in USD.
        change_24h (float): Price change over the last 24 hours (%).
        market_cap (float): Market capitalization in USD.
    """
    rank: int
    name: str
    symbol: str
    price_usd: float
    change_24h: float
    market_cap: float

    def as_row(self) -> tuple:
        """
        Converts the record to a tuple representation suitable for CSV/SQL writing.

        Returns:
            tuple[int, str, str, float, float, float]: Data as a flat row.
        """
        return (
            self.rank,
            self.name,
            self.symbol,
            self.price_usd,
            self.change_24h,
            self.market_cap,
        )
