import numpy as np
import numpy.typing as npt
from .core import Core


class ContinuousCore(Core):
    def __init__(self, total: float = 1):
        super().__init__(total=total, precision=0)

        
    def correct_weights(self, weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return weights