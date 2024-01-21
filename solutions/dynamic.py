from dtos import Flow, EMPTY_FLOW
from common import Core
from .solution import Solution
from .randomized import RandomizedSolution
from .targets import Target
from visualization import Listener, BlankListener, Change
from typing import Optional
import random


class DynamicSolution(Solution):
    def solve(self, core: Core, target: Target, starting: Optional[Flow] = None, iters: Optional[int] = 5, attach: Listener = BlankListener()) -> Flow:
        attach.on_start(self.graph, core)
        if not starting:
            flow = RandomizedSolution(self.graph).solve(core)
        else:
            flow = starting
        attach.on_iteration(flow, None)
        for _ in range(iters):
            candidates = {k:v for k,v in flow.paths.items() if v>0}
            random_source = random.choice(list(candidates.keys()))
            random_target = random.choice(list(self.graph.possible_paths()))
            new_flow=Flow.bump(Flow.dump(flow, random_source, core.precision), random_target, core.precision)
            if target.calc(flow,random_source)>target.calc(new_flow,random_target):
                flow=new_flow
                attach.on_iteration(flow, Change(path_increased=random_target, value=core.precision))
        attach.on_end()

        return Flow.correct_flow(flow, core.correct_values)