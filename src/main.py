#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Entry point for the helium potential project."""

from __future__ import annotations

import argparse
from pathlib import Path

from helium.grid import create_grid
from helium.model import potential
from helium.plotting import apply_plot_style, plot_1d_slice, plot_2d_field


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate helium potential visualizations.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--plot-type',
        choices=['1d', '2d', 'both'],
        default='both',
        help='Which plots to generate: 1d, 2d, or both (default: both).',
    )
    parser.add_argument(
        '--electron-distance',
        type=float,
        default=2.5,
        help='Default distance of the fixed electron along x-axis in Ångströms (default: 2.5).',
    )
    parser.add_argument(
        '--electron-distance-1d',
        type=float,
        default=None,
        help='Distance of the fixed electron for the 1D plot. Overrides --electron-distance if set.',
    )
    parser.add_argument(
        '--electron-distance-2d',
        type=float,
        default=None,
        help='Distance of the fixed electron for the 2D plot. Overrides --electron-distance if set.',
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('../output/plots'),
        help='Output directory for plots (default: ../output/plots)',
    )
    return parser.parse_args()


def main(
    plot_type: str = 'both',
    electron_distance: float = 2.5,
    electron_distance_1d: float | None = None,
    electron_distance_2d: float | None = None,
    output_dir: Path = Path('../output/plots'),
) -> None:
    """Create the grid, compute potentials, and save the plots.

    Parameters
    ----------
    electron_distance : float
        Position of the fixed electron along the x-axis in Ångströms.
    output_dir : Path
        Directory to save the output plots.
    """
    apply_plot_style()

    x, y, X, Y = create_grid()

    z = 0.0
    z2 = 0.0
    ZC = 2.0
    y2 = 0.0
    x2_inf = 3000.0

    electron_distance_1d = electron_distance_1d if electron_distance_1d is not None else electron_distance
    electron_distance_2d = electron_distance_2d if electron_distance_2d is not None else electron_distance

    pot_ref = potential(X, Y, z, x2_inf, y2, z2, ZC)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if plot_type in ('1d', 'both'):
        pot_1d = potential(X, Y, z, electron_distance_1d, y2, z2, ZC)
        plot_1d_path = plot_1d_slice(
            x,
            pot_ref,
            pot_1d,
            electron_distance=electron_distance_1d,
            output_dir=output_dir,
            y_index=len(y) // 2,
        )
        print(f"1D slice plot saved: {plot_1d_path}")

    if plot_type in ('2d', 'both'):
        pot_2d = potential(X, Y, z, electron_distance_2d, y2, z2, ZC)
        plot_2d_path = plot_2d_field(
            X,
            Y,
            pot_2d,
            electron_distance=electron_distance_2d,
            output_dir=output_dir,
        )
        print(f"2D field plot saved: {plot_2d_path}")


if __name__ == '__main__':
    args = parse_arguments()
    main(
        plot_type=args.plot_type,
        electron_distance=args.electron_distance,
        electron_distance_1d=args.electron_distance_1d,
        electron_distance_2d=args.electron_distance_2d,
        output_dir=args.output_dir,
    )
