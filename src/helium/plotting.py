#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Plotting helpers for helium potential visualizations."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def _configure_axes(
    ax: plt.Axes,
    x_label: str,
    y_label: str,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
) -> None:
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.grid(True)


def plot_1d_potential(
    x: np.ndarray,
    pot_ref: np.ndarray,
    pot: np.ndarray,
    y_index: int = 200,
    output_path: str = '1D-potential_static.png',
    x_label: str = r'$x$ [$\AA$]',
    y_label: str = 'Potential energy [a.u.]',
    xlim: tuple[float, float] = (-10.0, 10.0),
    ylim: tuple[float, float] = (-5.0, 5.0),
) -> None:
    """Generate and save a 1D potential comparison plot."""
    fig, ax = plt.subplots()
    ax.plot(x, pot_ref[:, y_index], label=r'$-2/r$', color='tab:red')
    ax.plot(x, pot[:, y_index], label=r'$-2/r + 1/r_2$', color='tab:blue')
    _configure_axes(ax, x_label, y_label, xlim, ylim)
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
    x_label: str = r'$x$ [$\AA$]',
    y_label: str = r'$y$ [$\AA$]',
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
    cbar.set_label('Potential energy [a.u.]', fontsize=10)
    cbar.ax.tick_params(labelsize=9)
    contours = ax.contour(
        X,
        Y,
        pot,
        levels=contour_levels,
        colors='black',
        linewidths=0.8,
    )
    ax.clabel(contours, inline=True, fontsize=8)
    _configure_axes(ax, x_label, y_label, xlim, ylim)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
