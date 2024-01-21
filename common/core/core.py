from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt

class Core(ABC):
    def __init__(self, *, total: float, precision: float):
        if total <= 0:
            raise ValueError(f"Total must be positive, got {total}")
        if precision < 0:
            raise ValueError(f"Precision must be non-negative, got {precision}")
        
        self.total = total
        self.precision = precision

    @abstractmethod
    def correct_values(self, weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        pass

    @abstractmethod
    def correct_value(self, weight: float) -> float:
        pass