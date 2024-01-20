from typing import Optional
from .listener import Change, Listener
from dtos import Graph, Flow
from common import Core

class Plotter(Listener):
    # TODO: Implement this class
    def on_start(self, graph: Graph, core: Core) -> None:
        pass

    def on_iteration(self, flow: Flow, change: Optional[Change]) -> None:
        print(change)
        flow.draw()

    def on_end(self) -> None:
        pass