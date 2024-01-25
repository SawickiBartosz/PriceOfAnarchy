from typing import Optional

import numpy as np
import scipy.optimize as opt
from dtos import Flow, EMPTY_FLOW, Graph
from common import Core, ContinuousCore
from .solution import Solution
from .randomized import RandomizedSolution
from .targets import Target, TargetOptimal
from visualization import Listener, BlankListener, Change


class NumericalSolution(Solution):
    def solve(self, core: Core, target: Target, attach: Listener = BlankListener(), seed: Optional[int] = None) -> Flow:
        if not isinstance(target, TargetOptimal):
            raise ValueError("Numerical optimization supported only for social optimum targets")
        if not isinstance(core, ContinuousCore):
            raise ValueError("Numerical optimization supported only for continuous case")
        attach.on_start(self.graph, core)
        random = np.random.default_rng(seed)
        p0 = RandomizedSolution(self.graph).solve(core, seed=random.integers(2e6)).to_numpy()
        attach.on_iteration(
            Flow(self.graph,
                 {path: p_flow for path, p_flow in zip(self.graph.possible_paths(), p0)}),
            None)
        def cost_function(p: np.array, g: Graph):
            paths = {path: p_flow for path, p_flow in zip(g.possible_paths(), p)}
            f = Flow(g, paths)
            return f.cost

        def callback(res):
            attach.on_iteration(
                Flow(self.graph,
                     {path: p_flow for path, p_flow in zip(self.graph.possible_paths(), res)}),
                None)

        sum_constraint = opt.LinearConstraint(np.ones_like(p0), [1], [1])
        bounds = opt.Bounds(np.zeros_like(p0), np.ones_like(p0))
        res = opt.minimize(cost_function,
                           p0,
                           args=self.graph,
                           bounds=bounds,
                           constraints=sum_constraint,
                           callback=callback)

        flow = Flow(self.graph, {path: p_flow for path, p_flow in zip(self.graph.possible_paths(), res.x)})
        attach.on_end()
        return Flow.correct_flow(flow, core.correct_values)
