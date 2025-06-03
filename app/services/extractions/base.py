from abc import ABC, abstractmethod
from typing import Any, List

from pydantic import BaseModel


class BaseExtractor(ABC):
    """
    Base class for all extraction classes.
    """

    def __init__(self) -> None:
        pass


    @abstractmethod
    def fetch_data(self, year: int) -> List[dict[str, str]]:
        """
        Fetch data from the given URL.
        """
        pass

    # @abstractmethod
    # def normalize(self, data: List[dict[str, str]]) -> List[dict[str, str]]:
    #     """
    #     Normalize the data extracted from the source.
    #     """
    #     pass