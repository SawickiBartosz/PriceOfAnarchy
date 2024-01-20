from abc import ABC, abstractmethod
from dtos import Flow, Graph
from .core import Core


class Solution(ABC):
    def __init__(self, graph: Graph):
        self.graph = graph
    
    @abstractmethod
    def solve(self, core: Core) -> Flow:
        pass