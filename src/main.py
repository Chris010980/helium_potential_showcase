#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Entry point for the helium potential project."""

from __future__ import annotations

import argparse
from pathlib import Path

from helium.grid import create_grid
from helium.model import potential
from helium.plotting import apply_plot_style, plot_1d_potential, plot_2d_potential


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate helium potential visualizations.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--electron-distance',
        type=float,
        default=2.5,
        help='Position of the fixed electron along x-axis in Ångströms (default: 2.5)',
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('../output/plots'),
        help='Output directory for plots (default: ../output/plots)',
    )
    return parser.parse_args()


def main(electron_distance: float = 2.5, output_dir: Path = Path('../output/plots')) -> None:
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
    x2 = electron_distance
    y2 = 0.0
    x2_inf = 3000.0

    pot_ref = potential(X, Y, z, x2_inf, y2, z2, ZC)
    pot = potential(X, Y, z, x2, y2, z2, ZC)

    output_dir.mkdir(parents=True, exist_ok=True)

    plot_1d_potential(
        x,
        pot_ref,
        pot,
        y_index=len(y) // 2,
        output_path=str(output_dir / '1D-potential_static.png'),
    )
    plot_2d_potential(
        X,
        Y,
        pot,
        output_path=str(output_dir / '2D-potential_static.png'),
    )


if __name__ == '__main__':
    args = parse_arguments()
    main(electron_distance=args.electron_distance, output_dir=args.output_dir)
