#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

#################
# Matplotlib RC #
#################

mpl.rcParams.update({
    "figure.figsize": (7, 5),
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
    "grid.alpha": 0.5,

    "savefig.bbox": "tight",
})

###############
# Functions  #
###############

def potential(x, y, z, x2, y2, z2, ZC):
    r = np.sqrt(x**2 + y**2 + z**2)
    r2 = np.sqrt((x - x2)**2 + (y - y2)**2 + (z - z2)**2)
    return -ZC / r + 1 / r2

##########
# Data  #
##########

# grid
x = np.arange(-10, 10, 0.05)
y = np.arange(-10, 10, 0.05)
X, Y = np.meshgrid(x, y, indexing="ij")

z = 0
z2 = 0

# nucleus charge
ZC = 2

# fixed electron position (in gewünschtem Bereich)
x2 = 2.5
y2 = 0.0

# reference: second electron at infinity
x2_inf = 3000.0

# potentials
pot_ref = potential(X, Y, z, x2_inf, y2, z2, ZC)
pot = potential(X, Y, z, x2, y2, z2, ZC)

###############
# 1D Plot    #
###############

fig, ax = plt.subplots()

ax.plot(x, pot_ref[:, 200], label=r"$-2/r$", color="tab:red")
ax.plot(x, pot[:, 200], label=r"$-2/r + 1/r_2$", color="tab:blue")

ax.set_xlabel(r"$x$ [$\AA$]")
ax.set_ylabel("Potential energy [a.u.]")

ax.set_xlim(-10, 10)
ax.set_ylim(-5, 5)

ax.grid(True)
ax.legend(loc="upper left")

ax.axis("on")

fig.savefig("1D-potential_static.png", dpi=200)
plt.close(fig)

###############
# 2D Plot    #
###############

fig, ax = plt.subplots()

pcm = ax.pcolormesh(
    X, Y, pot,
    cmap="seismic",
    vmin=-0.5, vmax=0.5,
    shading="auto"
)

cbar = fig.colorbar(
    pcm,
    ax=ax,
    fraction=0.046,
    pad=0.04
)
cbar.set_label("Potential energy [a.u.]", fontsize=10)
cbar.ax.tick_params(labelsize=9)

contours = ax.contour(
    X, Y, pot,
    levels=[-0.3, -0.2, -0.1, 0],
    colors="black",
    linewidths=0.8
)
ax.clabel(contours, inline=True, fontsize=8)

ax.set_xlabel(r"$x$ [$\AA$]")
ax.set_ylabel(r"$y$ [$\AA$]")

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

ax.axis("on")

fig.savefig("2D-potential_static.png", dpi=200)
plt.close(fig)
