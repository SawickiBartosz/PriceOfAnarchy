from .target import Target
from dtos import Flow
from typing import Optional

class TargetOptimal(Target):
    def calc(self, flow: Flow, path: Optional[tuple[str, ...]]) -> float:
        return flow.cost