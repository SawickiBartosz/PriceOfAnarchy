from typing import Callable, Optional, Type
from dtos import Graph, Flow
from solutions.solution import Solution
from common import Core
from solutions.targets import Target
from visualization import Listener, BlankListener
import matplotlib.pyplot as plt


class Context:
    def __init__(self, methods: dict[str, Type[Solution] | Callable]):
        self.methods = methods

    def run(self, graph: Graph, core: Core, target: Target, *, attach: Listener = BlankListener(), seed: Optional[int] = None) -> dict[str, Flow]:
        return {
            k: v(graph).solve(core, target, attach=attach, seed=seed)
            for k, v in self.methods.items()
        }
    
    def run_and_draw(self, graph: Graph, core: Core, target: Target, *, attach: Listener = BlankListener(), seed: Optional[int] = None) -> None:
        flows = self.run(graph, core, target, attach=attach, seed=seed)
        fig, axs = plt.subplots(1, len(flows), figsize=(6*len(flows), 4))
        for i, (name, flow) in enumerate(flows.items()):
            flow.draw(ax=axs[i])
            plt.sca(axs[i])
            plt.title(name)
        plt.show()