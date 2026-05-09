from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def point(x: float, y: float, z: float = 0.0) -> np.ndarray:
    """Create a Manim-compatible 3D point."""

    return np.array([x, y, z], dtype=float)


def as_point(values: Sequence[float]) -> np.ndarray:
    """Convert any numeric sequence into a 3D point."""

    if len(values) != 3:
        raise ValueError("A point must contain exactly three coordinates.")
    return np.array(values, dtype=float)
