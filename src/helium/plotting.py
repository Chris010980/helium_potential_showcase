#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Plotting helpers for helium potential visualizations."""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


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
) -> None:
    """Generate and save a 1D potential comparison plot."""
    fig, ax = plt.subplots()
    ax.plot(x, pot_ref[:, y_index], label=r'$-2/r$', color='tab:red')
    ax.plot(x, pot[:, y_index], label=r'$-2/r + 1/r_2$', color='tab:blue')
    _configure_axes(ax, x_label, y_label, xlim, ylim, grid=True, grid_alpha=0.2)
    ax.legend(loc='upper left')
    fig.savefig(output_path, dpi=200)
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
) -> None:
    """Generate and save a 2D potential colormap plot."""
    fig, ax = plt.subplots()
    pcm = ax.pcolormesh(
        X,
        Y,
        pot,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        shading='auto',
    )
    cbar = fig.colorbar(pcm, ax=ax, fraction=0.046, pad=0.04)
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
    _configure_axes(ax, x_label, y_label, xlim, ylim, grid=False)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
