from dtos.latency_functions import LatencyFunction
import networkx as nx


class Graph:
    def __init__(self, start: str, end: str, edges: list[tuple[str, str, LatencyFunction]]):
        self.start = start
        self.end = end

        self.G = nx.Graph()
        self.G.add_nodes_from({e[0] for e in edges} | {e[1] for e in edges})
        self.G.add_edges_from([(e[0], e[1], {'cost': e[2]}) for e in edges])

    def draw(self) -> 'Graph':
        nx.draw(self.G, with_labels=True)
        return self
    
    def possible_paths(self) -> list[list[str]]:
        return list(nx.all_simple_paths(self.G, self.start, self.end))