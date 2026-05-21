#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Grid generation utilities for the helium potential project."""

from __future__ import annotations

import numpy as np


def create_grid(
    x_min: float = -10.0,
    x_max: float = 10.0,
    x_step: float = 0.05,
    y_min: float = -10.0,
    y_max: float = 10.0,
    y_step: float = 0.05,
    indexing: str = "ij",
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return 1D coordinate arrays and a 2D meshgrid.

    Parameters
    ----------
    x_min, x_max, x_step:
        Range and step size for the x coordinate.
    y_min, y_max, y_step:
        Range and step size for the y coordinate.
    indexing:
        Meshgrid indexing convention, typically 'ij'.

    Returns
    -------
    x, y, X, Y:
        One-dimensional coordinate arrays and the corresponding 2D grid.
    """
    x = np.arange(x_min, x_max, x_step)
    y = np.arange(y_min, y_max, y_step)
    X, Y = np.meshgrid(x, y, indexing=indexing)
    return x, y, X, Y
