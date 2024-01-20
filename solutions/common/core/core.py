from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt

class Core(ABC):
    def __init__(self, *, total: float, precision: float):
        self.total = total
        self.precision = precision

    @abstractmethod
    def correct_weights(self, weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        pass