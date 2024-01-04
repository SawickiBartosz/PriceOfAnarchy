from typing import Callable


class LatencyFunction:
    def __init__(self, label: str, func: Callable[[int], int]):
        self.label = label
        self.func = func
    
    def __call__(self, x: int) -> int:
        return self.func(x)
    
    def __repr__(self) -> str:
        return self.label

class q(LatencyFunction):
    def __init__(self, a: int, b: int, c: int):
        label = " + ".join([f"{v if v!=1 or l=='' else ''}{l}" for v, l in list(zip([a, b, c], ["x^2", "x", ""])) if v != 0])
        super().__init__(label, lambda x: a * x ** 2 + b * x + c)