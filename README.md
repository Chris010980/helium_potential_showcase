# Effective Electron Potential in the Helium Atom

Visualization of the effective electron potential in the helium atom using a reduced two-electron model.

## Overview

The helium atom is the simplest multi-electron atomic system in which
electron–electron interaction plays an essential role. Unlike the hydrogen atom,
the Schrödinger equation can no longer be solved analytically in closed form
due to the Coulomb repulsion between the two electrons.

This project visualizes an effective one-electron potential obtained by fixing
the position of the second electron in space. The resulting potential field
illustrates screening and correlation effects in real space.

The project includes:

- 1D potential slices
- 2D potential visualizations
- animated evolution of the potential
- parameter variation of electron positions

---

## Physical Model

The effective potential is modeled as

:contentReference[oaicite:0]{index=0}

where:

- \( Z \) is the nuclear charge
- \( r \) is the position of the observed electron
- \( r_2 \) is the fixed position of the second electron

The first term describes the attractive Coulomb interaction with the nucleus,
while the second term represents electron–electron repulsion.

This simplified model allows the structure of the interaction potential to be
studied directly in coordinate space.

---

## Visualizations

### 1D Potential Slice

The one-dimensional plots show how the effective potential changes as the
second electron moves relative to the nucleus.

Observed effects include:

- asymptotic Coulomb behavior at large distances
- local distortion of the potential
- partial screening of the nuclear charge

### 2D Potential Slice

The two-dimensional visualizations illustrate the anisotropy introduced by
fixing the second electron at a specific spatial position.

Animations further demonstrate the continuous evolution of the effective
potential landscape.

---

## Methodology

The visualizations are generated numerically using:

- spatial grid construction
- evaluation of Coulomb interaction terms
- parametric variation of electron position
- visualization with Matplotlib
- frame-based animation rendering

---

## Repository Structure

```text
.
├── src/                # Python source code
├── src/main.py         # main.py
├── src/helium          # modules
├── output/plots        # Generated plots
├── output/videos       # Generated videos
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repo-url>
cd helium-potential
```

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Basic Usage

Generate both 1D and 2D plots with default settings:

```bash
python src/main.py
```

### Generate Static Plots Only

Create 1D and 2D potential visualizations without animation:

```bash
# Both 1D and 2D plots (default)
python src/main.py

# Only 1D plots
python src/main.py --plot-type 1d

# Only 2D plots
python src/main.py --plot-type 2d
```

### Customize Electron Positions

Override the fixed electron distance (default: 2.5 Ångströms):

```bash
# Global override
python src/main.py --electron-distance 3.0

# Separate 1D and 2D settings
python src/main.py --electron-distance-1d 2.0 --electron-distance-2d 4.0
```

### Generate Animation Frames and Videos

Create MP4 videos from animation frames with automatic cleanup:

```bash
# Generate 1D and 2D animations (default framerate: 20 fps)
python src/main.py --animate

# Only 1D animation
python src/main.py --animate --plot-type 1d

# Only 2D animation
python src/main.py --animate --plot-type 2d

# Custom framerate (e.g., 30 fps)
python src/main.py --animate --framerate 30
```

### Generate Frames Without Video Encoding

Create frame sequences without MP4 video generation (faster):

```bash
# Generate all frames (1D and 2D)
python src/main.py --frames-only

# Only 1D frames
python src/main.py --frames-only --plot-type 1d

# Keep frames after processing (useful for external video tools)
python src/main.py --frames-only --keep-frames
```

### Archive Frames as ZIP

Create compressed archives of frame directories:

```bash
# Generate frames and create ZIP archive (frames deleted after archiving)
python src/main.py --frames-only --zip-frames

# Keep frames and archive
python src/main.py --frames-only --zip-frames --keep-frames

# Generate videos and archive all frames before deletion
python src/main.py --animate --zip-frames
```

### Logging

Control logging verbosity and output:

```bash
# Default (INFO level)
python src/main.py --animate

# Debug level (detailed process information)
python src/main.py --animate --log-level DEBUG

# Warning level (only warnings and errors)
python src/main.py --animate --log-level WARNING
```

### Output Organization

Generated files are stored in the output directory structure:

```text
output/
├── plots/          # Static 1D and 2D plots
├── frames/
│   ├── 1d/         # 1D animation frames
│   └── 2d/         # 2D animation frames
├── videos/         # MP4 videos
logs/               # Timestamped log files
```

---

## Scientific Motivation

Understanding electron–electron interaction is fundamental for describing
real atomic systems.

This project serves as a visual and computational foundation for more advanced
approaches including:

- Hylleraas-type wavefunctions
- variational methods for helium
- explicit correlation models
- electron–electron cusp investigations

---

## Future Extensions

Possible future extensions include:

- full 3D visualization
- interactive parameter controls
- numerical solution of reduced Schrödinger models
- visualization of correlated wavefunctions
- comparison with Hartree–Fock approximations

---

## Technologies

- Python
- NumPy
- Matplotlib
- FFmpeg (video encoding)

---

## License

MIT License

---

## Author

Christian Lurz
