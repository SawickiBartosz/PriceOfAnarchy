import numpy as np
import numpy.typing as npt
import iteround
from .core import Core


class DiscreteCore(Core):
    def __init__(self, total: float, *, precision: float = 1):
        super().__init__(total=total, precision=precision)

    def correct_weights(self, weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return iteround.saferound(weights/self.precision, 0)*self.precision