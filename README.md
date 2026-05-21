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
├── notebooks/          # Optional exploratory notebooks
├── requirements.txt
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

Generate the plots:

```bash
python src/main.py
```

Generated figures and animations will be stored in the `assets/` directory.

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
