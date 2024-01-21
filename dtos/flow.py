from collections import defaultdict
from functools import cached_property
from typing import Callable, Optional
from matplotlib import pyplot as plt
import numpy as np
from const import EDGE_COLORMAP
from dtos import Graph

EMPTY_FLOW = object()

class Flow:
    def __init__(self, graph: Graph, paths: dict[tuple[str, ...], float]):
        self.graph = graph
        if paths is EMPTY_FLOW:
            self.paths = {path: 0 for path in self.graph.possible_paths()}
        else:
            self.paths = self._validate_paths(paths)

    def _validate_paths(self, paths: dict[tuple[str, ...], float]) -> dict[tuple[str, ...], float]:
        possible_paths = self.graph.possible_paths()
        for path in paths:
            if path not in possible_paths:
                raise ValueError(f"Path {path} is not a possible path in the graph.")
        
        unspecified_paths = [path for path in possible_paths if path not in paths]
        paths = {**paths, **{path: 0 for path in unspecified_paths}}
        if len(unspecified_paths) > 0:
            print(f"Warning: unspecified path{'s' if len(unspecified_paths) > 1 else ''} {unspecified_paths}, assuming 0.")

        min_load = min(paths.values())
        if min_load < 0:
            raise ValueError(f"Flow cannot have negative load, but has {min_load}.")

        max_load = max(paths.values())
        if max_load == 0:
            print(f"Warning: flow is empty, all paths have 0 load.")
        
        return paths

    def get_loads(self) -> dict[tuple[str, str], float]:
        loads = defaultdict(int)
        for path, flow in self.paths.items():
            for edge in Graph.split_path(path):
                loads[edge] += flow
        return dict(loads)
    
    @cached_property
    def cost(self) -> float:
        return sum([load * self.graph.get_latency(edge)(load) for edge, load in self.get_loads().items()])
    
    def path_cost(self, path: tuple[str, ...]) -> float:
        edges = Graph.split_path(path)
        return sum([self.graph.get_latency(edge)(load) for edge, load in self.get_loads().items() if edge in edges])

    def draw(self) -> 'Flow':
        loads = self.get_loads()
        max_load = max(loads.values())
        if max_load == 0:
            max_load = 1
        self.graph.draw(
            edge_labels={k: f"{v:.3g}" for k, v in loads.items()}, 
            edge_color={edge: EDGE_COLORMAP(1 - loads[edge] / max_load) for edge in loads},
            width={edge: 1+3*(loads[edge] / max_load) for edge in loads}
        )
        plt.legend(handles=[], title=f"Total cost: {self.cost:.5g}", loc='lower center')
        plt.show()
        return self

    def __repr__(self) -> str:
        return f"Flow(cost: {self.cost}, {self.paths})"
    
    @classmethod
    def bump(cls, flow: 'Flow', path: tuple[str, ...], amount: float, *, decrease: Optional[tuple[str, ...]] = None) -> 'Flow':
        if decrease == path:
            return flow
        
        paths = {**flow.paths, **{path: flow.paths[path] + amount}, **({decrease: flow.paths[decrease] - amount} if decrease is not None else {})}
        return cls(flow.graph, paths)
    
    @classmethod
    def dump(cls, flow: 'Flow', path: tuple[str, ...], amount: float) -> 'Flow':
        paths = {**flow.paths, **{path: flow.paths[path] - amount}}
        return cls(flow.graph, paths)
    
    @classmethod
    def correct_flow(cls, flow: 'Flow', func: Callable) -> 'Flow':
        values = func(np.array(list(flow.paths.values())))
        paths = {path: values[i] for i, path in enumerate(flow.paths)}
        return cls(flow.graph, paths)