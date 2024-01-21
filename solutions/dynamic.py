from dtos import Flow, EMPTY_FLOW
from common import Core
from .solution import Solution
from .randomized import RandomizedSolution
from .targets import Target
from visualization import Listener, BlankListener, Change
from typing import Optional
import numpy as np

class DynamicSolution(Solution):
    def solve(self, core: Core, target: Target, starting_flow: Optional[Flow] = None, starting_p: Optional[Flow] = 0.5, iters: Optional[int] = 500, seed: int = 2137, attach: Listener = BlankListener()) -> Flow:
        np.random.seed(seed)
        attach.on_start(self.graph, core)
        if not starting_flow:
            flow = RandomizedSolution(self.graph).solve(core, seed=seed)
        else:
            flow = starting_flow
        attach.on_iteration(flow, None)
        for time in range(iters):
            candidates = {k:v for k,v in flow.paths.items() if v>0}
            random_source = list(candidates.keys())[np.random.choice(np.arange(len(candidates.keys())))]
            random_target = list(self.graph.possible_paths())[np.random.choice(np.arange(len(self.graph.possible_paths())))]
            value = min(max(core.correct_values(np.array([starting_p*(1-time/iters)*candidates[random_source]]))[0],core.precision),candidates[random_source])
            new_flow=Flow.bump(Flow.dump(flow, random_source, value), random_target, value)
            diff = target.calc(flow,random_source)-target.calc(new_flow,random_target)
            if diff>=core.precision:
                flow=new_flow
                attach.on_iteration(flow, Change(path_increased=random_target, value=core.precision))
        attach.on_end()
        return Flow.correct_flow(flow, core.correct_values)