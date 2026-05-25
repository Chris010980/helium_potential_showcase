#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Animation pipeline utilities for helium potential visualizations."""

from __future__ import annotations

import logging
import subprocess
import zipfile
from pathlib import Path
from typing import Iterable

import numpy as np

from helium.model import potential
from helium.plotting import plot_1d_potential, plot_2d_potential

logger = logging.getLogger(__name__)


def ensure_frame_directories(base_dir: Path) -> tuple[Path, Path]:
    """Create and return the 1D and 2D frame directories."""
    frames_dir = base_dir / 'frames'
    one_d_dir = frames_dir / '1d'
    two_d_dir = frames_dir / '2d'
    one_d_dir.mkdir(parents=True, exist_ok=True)
    two_d_dir.mkdir(parents=True, exist_ok=True)
    logger.debug('Ensured animation frame directories: %s, %s', one_d_dir, two_d_dir)
    return one_d_dir, two_d_dir


def build_distance_sequence(
    start: float = 30.0,
    stop: float = 0.0,
    step: float = 0.05,
) -> np.ndarray:
    """Return a sequence of x2 distances for animation frames."""
    if start <= stop:
        raise ValueError('start must be larger than stop for a descending animation sequence.')
    sequence = np.arange(start, stop, -abs(step))
    logger.debug('Built distance sequence: start=%s stop=%s step=%s count=%d', start, stop, step, sequence.size)
    return sequence


def generate_1d_frames(
    x: np.ndarray,
    X: np.ndarray,
    Y: np.ndarray,
    pot_ref: np.ndarray,
    z: float,
    y2: float,
    z2: float,
    ZC: float,
    electron_distances: Iterable[float],
    frame_dir: Path,
    y_index: int | None = None,
) -> list[Path]:
    """Generate 1D animation frames and return the saved paths."""
    frame_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    logger.info('Generating %d 1D animation frames in %s', len(electron_distances), frame_dir)

    if y_index is None:
        y_index = pot_ref.shape[1] // 2

    for index, x2 in enumerate(electron_distances):
        pot = potential(X, Y, z, x2, y2, z2, ZC)
        output_path = frame_dir / f'frame_{index:04d}.png'
        title = rf'1D potential, fixed electron at {x2:.2f} Å'
        plot_1d_potential(
            x,
            pot_ref,
            pot,
            y_index=y_index,
            output_path=str(output_path),
            title=title,
        )
        paths.append(output_path)

    return paths


def generate_2d_frames(
    X: np.ndarray,
    Y: np.ndarray,
    z: float,
    y2: float,
    z2: float,
    ZC: float,
    electron_distances: Iterable[float],
    frame_dir: Path,
) -> list[Path]:
    """Generate 2D animation frames and return the saved paths."""
    frame_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    logger.info('Generating %d 2D animation frames in %s', len(electron_distances), frame_dir)

    for index, x2 in enumerate(electron_distances):
        pot = potential(X, Y, z, x2, y2, z2, ZC)
        output_path = frame_dir / f'frame_{index:04d}.png'
        title = rf'2D potential, fixed electron at {x2:.2f} Å'
        plot_2d_potential(
            X,
            Y,
            pot,
            output_path=str(output_path),
            title=title,
        )
        paths.append(output_path)

    return paths


def create_video(
    frames_dir: Path,
    output_path: Path,
    framerate: int = 20,
    pattern: str = 'frame_%04d.png',
) -> Path:
    """Create an MP4 video from a sequence of frame images."""
    output_path = output_path.with_suffix('.mp4')
    command = [
        'ffmpeg',
        '-y',
        '-framerate', str(framerate),
        '-i', str(frames_dir / pattern),
        '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        str(output_path),
    ]
    logger.info('Creating video %s from frames in %s at %d fps', output_path, frames_dir, framerate)
    logger.debug('Running ffmpeg command: %s', ' '.join(command))
    subprocess.run(command, check=True)
    return output_path


def zip_frames(frames_dir: Path, output_path: Path) -> Path:
    """Zip all PNG files in a frame directory."""
    output_path = output_path.with_suffix('.zip')
    logger.info('Zipping frames from %s into %s', frames_dir, output_path)
    with zipfile.ZipFile(output_path, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for frame in sorted(frames_dir.glob('*.png')):
            zipf.write(frame, frame.name)
    return output_path


def cleanup_frames(frames_dir: Path) -> None:
    """Delete all PNG frames in the given directory."""
    logger.info('Cleaning up %d frame files in %s', len(list(frames_dir.glob('*.png'))), frames_dir)
    for frame in frames_dir.glob('*.png'):
        frame.unlink()
