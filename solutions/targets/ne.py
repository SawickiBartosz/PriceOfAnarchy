from .target import Target
from dtos import Flow
from typing import Optional

class TargetNE(Target):
    def calc(self, flow: Flow, path: Optional[tuple[str, ...]]) -> float:
        if path is None:
            raise ValueError("TargetNE cannot be used without providing a path")
        return flow.path_cost(path)