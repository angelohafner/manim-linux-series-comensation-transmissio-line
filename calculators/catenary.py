from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def catenary_drop(alpha: float, sag: float, tension: float) -> float:
    """Return the vertical drop for a normalized catenary parameter."""

    centered_alpha = 2.0 * alpha - 1.0
    numerator = np.cosh(tension) - np.cosh(tension * centered_alpha)
    denominator = np.cosh(tension) - 1.0
    return float(sag * numerator / denominator)


def catenary_point(
    start: Sequence[float],
    end: Sequence[float],
    alpha: float,
    sag: float,
    tension: float,
) -> np.ndarray:
    """Return one point on a catenary span between two supports."""

    start_point = np.array(start, dtype=float)
    end_point = np.array(end, dtype=float)
    point = start_point + (end_point - start_point) * alpha
    point[1] -= catenary_drop(alpha, sag, tension)
    return point
