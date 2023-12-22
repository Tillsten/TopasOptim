from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

import numpy as np


class OptimizerModel(Protocol):
    """Protocol for optimizer models."""

    num_params: int

    def step(
        self,
        params: np.ndarray[Any, np.float64],
        func: Callable[[np.ndarray[Any, np.float64]], float],
    ) -> float:
        """Perform a step of the optimizer."""
        ...

    def get_history(self) -> np.ndarray[Any, float]:
        """Get the history of the optimizer."""
        ...
