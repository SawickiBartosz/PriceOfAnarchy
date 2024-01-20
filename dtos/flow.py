from collections import defaultdict
from functools import cached_property
from matplotlib import pyplot as plt
from const import EDGE_COLORMAP
from dtos import Graph

class Flow:
    def __init__(self, graph: Graph, paths: dict[tuple[str, ...], float]):
        possible_paths = graph.possible_paths()
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

        self.graph = graph
        self.paths = paths

    def get_loads(self) -> dict[tuple[str, str], float]:
        loads = defaultdict(int)
        for path, flow in self.paths.items():
            for edge in zip(path[:-1], path[1:]):
                loads[tuple(sorted(edge))] += flow
        return dict(loads)
    
    @cached_property
    def cost(self) -> float:
        return sum([load * self.graph.get_latency(edge)(load) for edge, load in self.get_loads().items()])

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