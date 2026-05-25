#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Plotting helpers for helium potential visualizations."""

from __future__ import annotations

import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable

logger = logging.getLogger(__name__)


def apply_plot_style() -> None:
    """Apply consistent plotting style across all figures."""
    mpl.rcParams.update({
        "figure.figsize": (7.8, 4.9),
        "figure.dpi": 150,
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "legend.frameon": False,
        "lines.linewidth": 1.8,
        "grid.linestyle": "dashed",
        "grid.alpha": 0.3,
        "grid.color": "0.6",
        "savefig.bbox": "tight",
    })
    logger.debug('Applied consistent plot style settings.')


def _configure_axes(
    ax: plt.Axes,
    x_label: str,
    y_label: str,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    grid: bool = True,
    grid_alpha: float = 0.3,
) -> None:
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if grid:
        ax.grid(True, alpha=grid_alpha, color="0.6")


def plot_1d_potential(
    x: np.ndarray,
    pot_ref: np.ndarray,
    pot: np.ndarray,
    y_index: int = 200,
    output_path: str = '1D-potential_static.png',
    x_label: str = r'$x$ ($\AA$)',
    y_label: str = 'Potential energy (a.u.)',
    xlim: tuple[float, float] = (-10.0, 10.0),
    ylim: tuple[float, float] = (-5.0, 5.0),
    title: str | None = None,
) -> None:
    """Generate and save a 1D potential comparison plot."""
    fig, ax = plt.subplots()
    ax.plot(x, pot_ref[:, y_index], label=r'$-2/r$', color='tab:red')
    ax.plot(x, pot[:, y_index], label=r'$-2/r + 1/r_2$', color='tab:blue')
    if title is not None:
        ax.set_title(title, pad=8)
    _configure_axes(ax, x_label, y_label, xlim, ylim, grid=True, grid_alpha=0.2)
    ax.legend(loc='upper left')
    fig.savefig(output_path, dpi=200)
    logger.info('Saved 1D potential plot to %s', output_path)
    plt.close(fig)



def plot_2d_potential(
    X: np.ndarray,
    Y: np.ndarray,
    pot: np.ndarray,
    output_path: str = '2D-potential_static.png',
    cmap: str = 'seismic',
    vmin: float = -0.5,
    vmax: float = 0.5,
    contour_levels: tuple[float, ...] = (-0.3, -0.2, -0.1, 0.0),
    x_label: str = r'$x$ ($\AA$)',
    y_label: str = r'$y$ ($\AA$)',
    xlim: tuple[float, float] = (-10.0, 10.0),
    ylim: tuple[float, float] = (-10.0, 10.0),
    title: str | None = None,
) -> None:
    """Generate and save a 2D potential colormap plot with equal aspect ratio."""
    fig, ax = plt.subplots(figsize=(9.5, 4.9))
    pcm = ax.pcolormesh(
        X,
        Y,
        pot,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        shading='auto',
    )
    
    # Enforce equal aspect ratio (1:1 scaling for x and y axes)
    ax.set_aspect('equal', adjustable='box')
    
    # Use make_axes_locatable for better colorbar placement
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='3.5%', pad=0.05)
    cbar = fig.colorbar(pcm, cax=cax)
    cbar.set_label('Potential energy (a.u.)', fontsize=10, color='0.3')
    cbar.ax.tick_params(colors='0.3', labelsize=9)
    cbar.outline.set_edgecolor('0.6')

    contours = ax.contour(
        X,
        Y,
        pot,
        levels=contour_levels,
        colors='0.3',
        linewidths=0.8,
    )
    ax.clabel(contours, inline=True, fontsize=8)
    if title is not None:
        ax.set_title(title, pad=8)
    _configure_axes(ax, x_label, y_label, xlim, ylim, grid=False)
    fig.savefig(output_path, dpi=200)
    logger.info('Saved 2D potential plot to %s', output_path)
    plt.close(fig)


def plot_1d_slice(
    x: np.ndarray,
    pot_ref: np.ndarray,
    pot: np.ndarray,
    electron_distance: float,
    output_dir: str | Path,
    y_index: int | None = None,
) -> Path:
    """Generate and save a representative 1D potential slice.

    Parameters
    ----------
    x, pot_ref, pot : arrays
        Coordinate array and potential arrays.
    electron_distance : float
        Position of the fixed electron in Ångströms.
    output_dir : str or Path
        Directory to save the plot.
    y_index : int, optional
        Index for the y-coordinate slice. If None, uses the middle.

    Returns
    -------
    Path
        Path to the generated plot file.
    """
    if y_index is None:
        y_index = pot.shape[1] // 2

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"1D_slice_x2_{electron_distance:.2f}.png"
    output_path = output_dir / filename

    plot_1d_potential(
        x,
        pot_ref,
        pot,
        y_index=y_index,
        output_path=str(output_path),
    )

    return output_path


def plot_2d_field(
    X: np.ndarray,
    Y: np.ndarray,
    pot: np.ndarray,
    electron_distance: float,
    output_dir: str | Path,
) -> Path:
    """Generate and save a representative 2D potential field.

    Parameters
    ----------
    X, Y, pot : arrays
        Coordinate grids and potential array.
    electron_distance : float
        Position of the fixed electron in Ångströms.
    output_dir : str or Path
        Directory to save the plot.

    Returns
    -------
    Path
        Path to the generated plot file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"2D_field_x2_{electron_distance:.2f}.png"
    output_path = output_dir / filename

    plot_2d_potential(
        X,
        Y,
        pot,
        output_path=str(output_path),
    )

    return output_path
