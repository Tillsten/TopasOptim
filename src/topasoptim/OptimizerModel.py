from __future__ import annotations

from typing import Protocol

import numpy as np


class OptimizerModel(Protocol):
    """Protocol for optimizer models."""

    num_params: int

    def step(self, params: np.ndarray, func: callable) -> float:
        """Perform a step of the optimizer."""
        ...

    def get_history(self) -> np.ndarray:
        """Get the history of the optimizer."""
        ...
