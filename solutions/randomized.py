from typing import Optional
from dtos import Flow
from .targets import Target
from .common import Solution, Core
from numpy.random import default_rng


class RandomizedSolution(Solution):
    def solve(self, core: Core, target: Optional[Target] = None, *, seed: int = None) -> Flow:
        random = default_rng(seed)
        paths = self.graph.possible_paths()
        path_weights = random.uniform(0, 1, size=len(paths))
        path_weights = path_weights / path_weights.sum() * core.total
        path_weights = core.correct_values(path_weights)
        flow = Flow(self.graph, {path: path_weights[i] for i, path in enumerate(paths)})
        return flow