#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Helium model functions."""

from __future__ import annotations

import logging
import numpy as np

logger = logging.getLogger(__name__)


def potential(
    x: np.ndarray,
    y: np.ndarray,
    z: float,
    x2: float,
    y2: float,
    z2: float,
    ZC: float,
) -> np.ndarray:
    """Return the helium-like potential for a fixed second electron.

    The potential is defined as
        V = -ZC / r + 1 / r2
    where r is the distance to the nucleus and r2 is the distance to the fixed
    second electron.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            'Evaluating potential with x2=%.3f, y2=%.3f, z2=%.3f, grid shape=%s',
            x2,
            y2,
            z2,
            x.shape,
        )
    r = np.sqrt(x**2 + y**2 + z**2)
    r2 = np.sqrt((x - x2) ** 2 + (y - y2) ** 2 + (z - z2) ** 2)
    return -ZC / r + 1 / r2
