from dtos import Flow, EMPTY_FLOW
from .common import Solution, Core
from .targets import Target


class GreedySolution(Solution):
    def solve(self, core: Core, target: Target) -> Flow:
        flow = Flow(self.graph, EMPTY_FLOW)
        for _ in range(int(core.total/core.precision)):
            candidates = [(Flow.bump(flow, path, core.precision), path) for path in self.graph.possible_paths()]
            scores = [target.calc(*candidate) for candidate in candidates]
            best = min(zip(candidates, scores), key=lambda x: x[1])
            flow = best[0][0]
        return Flow.correct_flow(flow, core.correct_values)