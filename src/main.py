#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Entry point for the helium potential project."""

from __future__ import annotations

import argparse
import logging
from datetime import datetime
from pathlib import Path

from helium.animation import (
    build_distance_sequence,
    cleanup_frames,
    create_video,
    ensure_frame_directories,
    generate_1d_frames,
    generate_2d_frames,
    zip_frames,
)
from helium.grid import create_grid
from helium.model import potential
from helium.plotting import apply_plot_style, plot_1d_slice, plot_2d_field

# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_OUTPUT_DIR = PROJECT_ROOT / 'output'
DEFAULT_LOG_DIR = PROJECT_ROOT / 'logs'


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
        default=None,
        help='Base output directory for plots, frames, and videos (default: <project_root>/output).',
    )
    parser.add_argument(
        '--animate',
        action='store_true',
        help='Generate animation frames and create MP4 videos.',
    )
    parser.add_argument(
        '--frames-only',
        action='store_true',
        help='Generate animation frames without creating MP4 videos.',
    )
    parser.add_argument(
        '--no-animation',
        action='store_true',
        help='Alias for --frames-only. Use when you want frames only and no video.',
    )
    parser.add_argument(
        '--keep-frames',
        action='store_true',
        help='Retain generated frame PNGs after video creation.',
    )
    parser.add_argument(
        '--zip-frames',
        action='store_true',
        help='Create zip archives for generated frame directories.',
    )
    parser.add_argument(
        '--framerate',
        type=int,
        default=20,
        help='Framerate for created MP4 videos (default: 20).',
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Logging level for console and file output (default: INFO).',
    )
    return parser.parse_args()


def configure_logging(log_dir: Path, level: int = logging.INFO) -> Path:
    """Configure root logging and return the created log file path."""
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_path = log_dir / f'helium_potential_{timestamp}.log'

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return log_path


def main(
    plot_type: str = 'both',
    electron_distance: float = 2.5,
    electron_distance_1d: float | None = None,
    electron_distance_2d: float | None = None,
    output_dir: Path | None = None,
    animate: bool = False,
    frames_only: bool = False,
    keep_frames: bool = False,
    zip_frames_flag: bool = False,
    framerate: int = 20,
) -> None:
    """Create static plots or animation frames and videos.

    Parameters
    ----------
    plot_type : str
        Which plot types to generate: 1d, 2d, or both.
    electron_distance : float
        Default position of the fixed electron along the x-axis in Ångströms.
    electron_distance_1d : float | None
        Distance for the 1D plot.
    electron_distance_2d : float | None
        Distance for the 2D plot.
    output_dir : Path | None
        Base directory for plots, frames, and videos. If None, defaults to <project_root>/output.
    animate : bool
        Create animation videos from generated frames.
    frames_only : bool
        Generate frames without creating video.
    keep_frames : bool
        Keep frame PNGs after video creation.
    zip_frames_flag : bool
        Create zip archives for frame directories.
    framerate : int
        Target framerate for MP4 video creation.
    """
    logger = logging.getLogger(__name__)

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    if animate and frames_only:
        raise ValueError('Cannot use --animate and --frames-only together.')

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
    output_base = Path(output_dir)
    output_base.mkdir(parents=True, exist_ok=True)

    plots_dir = output_base / 'plots'
    plots_dir.mkdir(parents=True, exist_ok=True)

    if not animate and not frames_only:
        if plot_type in ('1d', 'both'):
            pot_1d = potential(X, Y, z, electron_distance_1d, y2, z2, ZC)
            plot_1d_path = plot_1d_slice(
                x,
                pot_ref,
                pot_1d,
                electron_distance=electron_distance_1d,
                output_dir=plots_dir,
                y_index=pot_1d.shape[1] // 2,
            )
            logger.info('1D slice plot saved: %s', plot_1d_path)

        if plot_type in ('2d', 'both'):
            pot_2d = potential(X, Y, z, electron_distance_2d, y2, z2, ZC)
            plot_2d_path = plot_2d_field(
                X,
                Y,
                pot_2d,
                electron_distance=electron_distance_2d,
                output_dir=plots_dir,
            )
            logger.info('2D field plot saved: %s', plot_2d_path)
        return

    videos_dir = output_base / 'videos'
    videos_dir.mkdir(parents=True, exist_ok=True)
    one_d_dir, two_d_dir = ensure_frame_directories(output_base)

    distances = build_distance_sequence()

    if plot_type in ('1d', 'both'):
        one_d_paths = generate_1d_frames(
            x,
            X,
            Y,
            pot_ref,
            z,
            y2,
            z2,
            ZC,
            distances,
            one_d_dir,
            y_index=pot_ref.shape[1] // 2,
        )
        logger.info('1D animation frames generated: %d files in %s', len(one_d_paths), one_d_dir)
        if animate:
            video_path = create_video(
                one_d_dir,
                videos_dir / f'1D_animation',
                framerate=framerate,
            )
            logger.info('1D video created: %s', video_path)
        if zip_frames_flag:
            zip_path = zip_frames(one_d_dir, one_d_dir.parent / '1d_frames')
            logger.info('1D frame archive created: %s', zip_path)
        if not keep_frames and (animate or zip_frames_flag):
            cleanup_frames(one_d_dir)

    if plot_type in ('2d', 'both'):
        two_d_paths = generate_2d_frames(
            X,
            Y,
            z,
            y2,
            z2,
            ZC,
            distances,
            two_d_dir,
        )
        logger.info('2D animation frames generated: %d files in %s', len(two_d_paths), two_d_dir)
        if animate:
            video_path = create_video(
                two_d_dir,
                videos_dir / f'2D_animation',
                framerate=framerate,
            )
            logger.info('2D video created: %s', video_path)
        if zip_frames_flag:
            zip_path = zip_frames(two_d_dir, two_d_dir.parent / '2d_frames')
            logger.info('2D frame archive created: %s', zip_path)
        if not keep_frames and (animate or zip_frames_flag):
            cleanup_frames(two_d_dir)


if __name__ == '__main__':
    args = parse_arguments()
    log_dir = DEFAULT_LOG_DIR
    log_path = configure_logging(log_dir, level=getattr(logging, args.log_level))
    logging.getLogger(__name__).info('Logging started. Log file: %s', log_path)

    main(
        plot_type=args.plot_type,
        electron_distance=args.electron_distance,
        electron_distance_1d=args.electron_distance_1d,
        electron_distance_2d=args.electron_distance_2d,
        output_dir=args.output_dir,
        animate=args.animate,
        frames_only=args.frames_only or args.no_animation,
        keep_frames=args.keep_frames,
        zip_frames_flag=args.zip_frames,
        framerate=args.framerate,
    )
