from typing import Optional
from .listener import Change, Listener
from dtos import Graph, Flow
from common import Core

class BlankListener(Listener):
    def on_start(self, graph: Graph, core: Core) -> None:
        pass

    def on_iteration(self, flow: Flow, change: Optional[Change]) -> None:
        pass

    def on_end(self) -> None:
        pass