from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel
from dtos import Graph, Flow
from common.core import Core

class Change(BaseModel):
    path_increased: tuple[str, ...]
    value: float
    path_decreased: Optional[tuple[str, ...]] = None

class Listener(ABC):
    @abstractmethod
    def on_start(self, graph: Graph, core: 'Core') -> None:
        pass

    @abstractmethod
    def on_iteration(self, flow: Flow, change: Optional[Change]) -> None:
        pass

    @abstractmethod
    def on_end(self) -> None:
        pass