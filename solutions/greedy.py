from dtos import Flow, EMPTY_FLOW
from common import Core
from .solution import Solution
from .targets import Target
from visualization import Listener, BlankListener, Change


class GreedySolution(Solution):
    def solve(self, core: Core, target: Target, attach: Listener = BlankListener()) -> Flow:
        attach.on_start(self.graph, core)
        flow = Flow(self.graph, EMPTY_FLOW)
        attach.on_iteration(flow, None)

        for _ in range(int(core.total/core.precision)):
            candidates = [(Flow.bump(flow, path, core.precision), path) for path in self.graph.possible_paths()]
            scores = [target.calc(*candidate) for candidate in candidates]
            best = min(zip(candidates, scores), key=lambda x: x[1])
            flow = best[0][0]
            attach.on_iteration(flow, Change(path_increased=best[0][1], value=core.precision))
        attach.on_end()

        return Flow.correct_flow(flow, core.correct_values)