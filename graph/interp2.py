#!/usr/bin/env python

import os
from shutil import rmtree
import matplotlib.pyplot as plt
import numpy as np
import cv2
import dcoloring, render
from funcs import *

WIDTH = 16
HEIGHT = 16
POINTS_PER_DIM = 2048
FRAMES = 480
FPS = 60
BACK_FORTH = True
TEMP_DIR = 'temp2'
OUT_DIR = 'out2'

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

x, y = np.ogrid[
    -WIDTH/2:WIDTH/2:POINTS_PER_DIM*1j,
    -HEIGHT/2:HEIGHT/2:POINTS_PER_DIM*1j
]
z = x + 1j*y

# 0 to 1 inclusive
lerp = np.arange(0.0, 1.0 + 1.0/FRAMES/2, 1.0/FRAMES)
cerp = dcoloring.cos_interpolation(lerp)
ucircle = np.exp(2j * np.pi * lerp)

# func_name = 'z^unitcircle'
func_name = "Soft Exponential"
print('Processing {}'.format(func_name))

# Perpare plots and function

fig = plt.figure()
ax = fig.add_subplot(111)


# Set interpolation and animate transition between two complex functions

file_names = []
path = OUT_DIR + '/' + func_name
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

log_base = 2.0  # np.exp(2*np.pi/6)
for idx in range(0, len(cerp)):
    c = 2 * cerp[idx] - 1
    if idx == FRAMES/2:
        c = 0.0
    w = soft_exponential(c, z)

    cfunc_plot = dcoloring.colorize(w, log_base=log_base, grid=False)

    ax.clear()
    ax.imshow(cfunc_plot, extent=(-WIDTH/2, WIDTH/2, -HEIGHT/2, HEIGHT/2))
    ax.set(title='Soft Exponential f({: 4.2f}, z)'.format(round(c, 2)))

    # Save frame
    print('Rendering frame {0:{2}}/{1:{2}}'.format(idx, FRAMES, int(np.log10(FRAMES) + 1)))
    temp_path = '{}/frame.{}.png'.format(TEMP_DIR, idx)
    fig.savefig(temp_path, dpi=1000, transparent=True)
    file_names.append(temp_path)

    # Resize for aliasing
    img = cv2.imread(temp_path)
    img = cv2.resize(img, (int(img.shape[1]/8), int(img.shape[0]/8)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(temp_path, img)

    # Save image of complete function
    if idx in (0, 120, 240, 360):
        img_path = '{}.{}.png'.format(path, idx)
        fig.savefig(img_path, dpi=1600, transparent=True)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)), interpolation=cv2.INTER_AREA)
        cv2.imwrite('{}.{}.png'.format(path, idx), img)

if BACK_FORTH:
    file_names = file_names + list(reversed(file_names[1:-1]))

print("Rendering {} frames to {}".format(len(file_names), path))
render.create_webm(path + ".8162", file_names, fps=FPS, bitrate='8162k')
render.create_webm(path + ".2048", file_names, fps=FPS, bitrate='2048k')
render.create_webm(path + ".1536", file_names, fps=FPS, bitrate='2048k')
render.create_webm(path + ".1024", file_names, fps=FPS, bitrate='1024k')
rmtree(TEMP_DIR)
plt.close('all')
