from dtos.latency_functions import LatencyFunction
import networkx as nx

COLORS = {"node": "#9293df", "flag": "#ffa45e"}

class Graph:
    def __init__(self, start: str, end: str, edges: list[tuple[str, str, LatencyFunction]]):
        self.start = start
        self.end = end

        self.G = nx.Graph()
        self.G.add_nodes_from(sorted({e[0] for e in edges} | {e[1] for e in edges}))
        self.G.add_edges_from([(e[0], e[1], {'cost': e[2]}) for e in edges])

    def draw(self) -> 'Graph':
        # color nodes
        pos = nx.spring_layout(self.G, seed=42)
        nx.draw(self.G, with_labels=True, pos=pos, node_color=[COLORS['flag'] if n in [self.start, self.end] else COLORS['node'] for n in self.G.nodes])
        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=nx.get_edge_attributes(self.G, 'cost'))
        return self
    
    def possible_paths(self) -> list[list[str]]:
        return list(nx.all_simple_paths(self.G, self.start, self.end))