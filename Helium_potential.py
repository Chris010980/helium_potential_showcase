#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 16:07:49 2021

@author: christian
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import ffmpeg
import zipfile
from os.path import basename
import matplotlib as mpl

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
#             #
#  Functions  #
#             #
###############

# Zip the files from given directory that matches the filter
def zipFilesInDir(dirName, zipFileName, filter):
   # create a ZipFile object
   zipf = zipfile.ZipFile(zipFileName, mode='w', compression=zipfile.ZIP_DEFLATED,  compresslevel=9)
   with zipf as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(dirName):
           for filename in filenames:
               if filter(filename):
                   # create complete filepath of file in directory
                   filePath = os.path.join(folderName, filename)
                   # Add file to zip
                   zipObj.write(filePath, basename(filePath))

# potential with positive core and fixed 2nd electron
def potential(x, y, z, x2, y2, z2, ZC):
    r=np.sqrt(x**2+y**2+z**2)
    r2=np.sqrt((x-x2)**2+(y-y2)**2+(z-z2)**2)
    return -ZC/r+1/r2

##########
#        #
#  Data  #
#        #
##########

# define data-points along x- and y-direction
x = np.arange(-10,10,0.05)
y = np.arange(-10,10,0.05)

# define 2D grid
X,Y = np.meshgrid(x,y, indexing='ij')

# set z/z2=0
z=0
z2=0

# position of the second electron
x2=5
y2=0

# Charge of the nucleus
ZC=2

# for comparison: second electron at "infinity"
x2_inf=3000

# calculate potentials
pot2 = potential(X,Y,z,x2_inf,y2,z2,ZC)


x2 = np.arange(30,0,-0.05)
xLength = len(x2)

# create directory to store plots and movie
if not os.path.exists('Figures'):
    os.makedirs('Figures')

for ind in range(xLength):
    # calculate potential
    pot = potential(X,Y,z,x2[ind],y2,z2,ZC)

    # 1D-plot
    fig, ax = plt.subplots()

    ax.plot(x, pot2[:,200], label=r"$-2/r$", color="tab:red")
    ax.plot(x, pot[:,200], label=r"$-2/r + 1/r_2$", color="tab:blue")

    ax.set_xlabel(r"$x$ [$\AA$]")
    ax.set_ylabel("Potential energy [a.u.]")

    ax.set_xlim(-10, 10)
    ax.set_ylim(-5, 5)

    ax.grid(True)
    ax.legend(loc="upper left")

    ax.set_title(
        rf"1D potential, fixed electron at {int(x2[ind])} $\AA$",
        pad=8
    )

    fig.savefig(
        f"Figures/1D-Pot_{ind:03d}.png",
        dpi=200
    )
    plt.close(fig)

# create movie
(
    ffmpeg
    .input('./Figures/*.png', pattern_type='glob', framerate=20)
    .output('1D-potential.mp4')
    .overwrite_output()
    .run()
)

# zip png files
zipFilesInDir('./Figures', './Figures/1D-potential.zip', lambda name : 'png' in name)

# remove the pngs
for pic in os.listdir('./Figures'):
    if pic.endswith('.png'):
        os.remove('./Figures/'+pic)

for ind in range(xLength):
    # calculate potential
    pot = potential(X,Y,z,x2[ind],y2,z2,ZC)

    # 2D-plot
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

    fig.suptitle(
        rf"2D potential, fixed electron at {int(x2[ind])} $\AA$",
        fontsize=13,
        y=0.97
    )

    fig.savefig(
        f"Figures/2D-Pot_{ind:03d}.png",
        dpi=200
    )
    plt.close(fig)

# create movie
(
    ffmpeg
    .input('./Figures/*.png', pattern_type='glob', framerate=20)
    .output('2D-potential.mp4')
    .overwrite_output()
    .run()
)

# zip png files
zipFilesInDir('./Figures', './Figures/2D-potential.zip', lambda name : 'png' in name)

# remove the pngs
for pic in os.listdir('./Figures'):
    if pic.endswith('.png'):
        os.remove('./Figures/'+pic)
