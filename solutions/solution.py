from abc import ABC, abstractmethod
from typing import Callable, Optional
from dtos import Flow, Graph
from solutions.targets import Target
from visualization import Listener, BlankListener
from common.core import Core


class Solution(ABC):
    def __init__(self, graph: Graph):
        self.graph = graph
    
    @abstractmethod
    def solve(self, core: Core, target: Target, *, attach: Listener = BlankListener(), seed: Optional[int] = None) -> Flow:
        pass

    @classmethod
    def parametrize(cls, **kwargs) -> Callable[[Graph], 'Solution']:
        return lambda graph: cls(graph, **kwargs)