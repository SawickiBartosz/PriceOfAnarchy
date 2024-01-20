from dtos import Flow, EMPTY_FLOW, Graph
from common import Core
from .solution import Solution
from .targets import Target
from visualization import Listener, BlankListener, Change


class RotatingGreedySolution(Solution):
    def __init__(self, graph: Graph, *, rotations: int = 1):
        super().__init__(graph)
        self.rotations = rotations

    def solve(self, core: Core, target: Target, attach: Listener = BlankListener()) -> Flow:
        attach.on_start(self.graph, core)
        flow = Flow(self.graph, EMPTY_FLOW)
        attach.on_iteration(flow, None)

        history = []
        for _ in range(int(core.total/core.precision)):
            candidates = [(Flow.bump(flow, path, core.precision), path) for path in self.graph.possible_paths()]
            scores = [target.calc(*candidate) for candidate in candidates]
            best = min(zip(candidates, scores), key=lambda x: x[1])
            flow = best[0][0]
            history.append(best[0][1])
            attach.on_iteration(flow, Change(path_increased=best[0][1], value=core.precision))
        
        for _ in range(self.rotations):
            for old_path in history:
                candidates = [(Flow.bump(flow, path, core.precision, decrease=old_path), path) for path in self.graph.possible_paths()]
                scores = [target.calc(*candidate) for candidate in candidates]
                best = min(zip(candidates, scores), key=lambda x: x[1])
                flow = best[0][0]
                if best[0][1] != old_path:
                    attach.on_iteration(flow, Change(path_increased=best[0][1], value=core.precision, path_decreased=old_path))
        
        attach.on_end()

        return Flow.correct_flow(flow, core.correct_values)