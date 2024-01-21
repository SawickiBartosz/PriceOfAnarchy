from typing import Optional, TypeVar
import networkx as nx
from const import FLAG_COLOR, NODE_COLOR
from dtos.latency_functions import LatencyFunction, q

T = TypeVar('T')
EdgeDict = dict[tuple[str, str], T]

class Graph:
    def __init__(self, start: str, end: str, edges: list[tuple[str, str, LatencyFunction]]):
        self.start = start
        self.end = end

        self.G = nx.Graph()
        nodes = set()
        repetitive = set()
        for e in edges:
            curr = (e[0],e[1]) if e[0]<e[1] else (e[1],e[0])
            if curr in nodes:
                repetitive.add(f"{curr[0]}'")
            else:
                nodes.add(curr)
        self.G.add_nodes_from(sorted({e[0] for e in edges} | {e[1] for e in edges} | repetitive))
        for edge in edges:
            self.add_edge_with_artificial_nodes(edge)
         
    def add_edge_with_artificial_nodes(self, edge: tuple[str, str, LatencyFunction]):
        source, target, latency_function = edge
        if source>target:
            source,target = target,source 
        if self.G.has_edge(source, target):
            artificial_node = f"{source}'"
            self.G.add_edge(source, artificial_node, cost=latency_function)
            self.G.add_edge(artificial_node, target, cost=q(0, 0, 0))
        else:
            self.G.add_edge(source, target, cost=latency_function)

    def draw(self, *, edge_labels: Optional[EdgeDict[str]] = None, edge_color: Optional[EdgeDict[str]] = None, width: Optional[EdgeDict[float]] = None) -> 'Graph':
        def dict_to_list(d: Optional[EdgeDict[any]]) -> list[any]:
            return [d[k] for k in self.G.edges()] if d is not None else None
        
        pos = nx.spring_layout(self.G, seed=42)
        nx.draw(
            self.G, with_labels=True, pos=pos, 
            node_color=[FLAG_COLOR if n in [self.start, self.end] else NODE_COLOR for n in self.G.nodes],
            edge_color=dict_to_list(edge_color), width=dict_to_list(width)
        )

        labels = nx.get_edge_attributes(self.G, 'cost')
        if edge_labels is not None:
            labels = {k: f"{v}\n{edge_labels[k]}" for k, v in labels.items()}
        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=labels)

        return self
    
    def get_latency(self, edge: tuple[str, str]) -> LatencyFunction:
        return self.G.get_edge_data(*edge)['cost']

    def possible_paths(self) -> list[list[str]]:
        return [tuple(path) for path in nx.all_simple_paths(self.G, self.start, self.end)]
    
    @classmethod
    def split_path(cls, path: tuple[str, ...]) -> list[tuple[str, str]]:
        return [tuple(sorted((path[i], path[i+1]))) for i in range(len(path)-1)]