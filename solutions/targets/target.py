from abc import ABC, abstractmethod
from typing import Optional

from dtos import Flow


class Target(ABC):
    @abstractmethod
    def calc(self, flow: Flow, path: Optional[tuple[str, ...]]) -> float:
        pass