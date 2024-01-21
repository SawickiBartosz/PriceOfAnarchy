import numpy as np
import numpy.typing as npt
import iteround
from .core import Core


class DiscreteCore(Core):
    def __init__(self, total: float, *, precision: float = 1):
        if total / precision % 1 != 0:
            raise ValueError(f"Total {total} is not a multiple of precision {precision}.")

        super().__init__(total=total, precision=precision)

    def correct_values(self, weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return np.array(iteround.saferound(weights/self.precision, 0))*self.precision
    
    def correct_value(self, weight: float) -> float:
        return round(weight/self.precision)*self.precision