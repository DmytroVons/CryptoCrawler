from abc import ABC, abstractmethod
from typing import Iterable
from core.models import CoinRecord

class DataScraper(ABC):
    """
    Abstract interface for cryptocurrency data scrapers.
    """

    @abstractmethod
    def scrape(self) -> Iterable[CoinRecord]:
        """
        Scrapes coin data and returns an iterable of CoinRecord objects.

        Returns:
            Iterable[CoinRecord]: Parsed coin data.
        """
        raise NotImplementedError
