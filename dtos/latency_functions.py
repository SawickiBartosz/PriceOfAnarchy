from typing import Callable
import numpy as np
from numpy.polynomial import Polynomial
import re


class LatencyFunction:
    def __init__(self, label: str, func: Callable[[int], int]):
        self.label = label
        self.func = func
    
    def __call__(self, x: int) -> int:
        return self.func(x)
    
    def __repr__(self) -> str:
        return self.label

class poly(LatencyFunction):
    def __init__(self, *coeffs):
        np.polynomial.set_default_printstyle('ascii')
        p = Polynomial(coeffs[::-1])
        label = str(p)
        label = re.sub(r'\+ 0.0 [^+]+', '', label)
        label = re.sub(r'^0.0 \+ ', '', label)
        label = re.sub(r'(^| )1.0+ x', 'x', label)
        label = re.sub(r'\.0+($| )', '', label)
        label = label.replace(' x', 'x').replace('**', '^')
        super().__init__(label, p)
        
class q(poly):
    def __init__(self, a: int, b: int, c: int):
        super().__init__(a, b, c)