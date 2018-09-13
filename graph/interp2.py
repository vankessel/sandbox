#!/usr/bin/env python

import os
from shutil import rmtree
import matplotlib.pyplot as plt
import numpy as np
import cv2
import dcoloring, render

FILE_NAME = 'exp(z)'
WIDTH = 16
HEIGHT = 16
POINTS_PER_DIM = 2048
FRAMES = 480
FPS = 60
BACK_FORTH = False
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
lerp = np.arange(0.0, 1.0 - 1.0/FRAMES/2, 1.0/FRAMES)
cerp = dcoloring.cos_interpolation(lerp)
ucircle = np.exp(2j * np.pi * lerp)

cfunctions = [
    # ('exp(z)', np.exp(z)),
    # ('ln(z)', np.log(z)),
    # ('z^3', z*z*z),
    # ('z^2', z*z),
    # ('z^0.5', np.sqrt(z)),
    # ('z^-1', 1/z),
    # ('z^-0.5', 1/np.sqrt(z)),
    # ('z^-2', 1/(z*z)),
    # ('sin(z)', np.sin(z)),
    # ('sinh(z)', np.sinh(z)),
    # ('asin(z)', np.arcsin(z)),
    # ('tan(z)', np.tan(z)),
    # ('Zoomed sin(z^-1)', np.sin(1/z)),
    # ('Zoomed tan(z^-1)', np.tan(1/z)),
    # ('z^2i', np.power(z, 2j)),
    # ('z^i', np.power(z, 1j)),
    # ('z^-i', np.power(z, -1j)),
    # ('z^-2i', np.power(z, -2j))
    ('z^')
]

func_name = 'unitcircle^z'
print('Processing {}'.format(func_name))

# Perpare plots and function

fig = plt.figure()
ax = fig.add_subplot(111)


# Set interpolation and animate transition between two complex functions

file_names = []
path = OUT_DIR + '/' + func_name
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

interp = cerp
for idx in range(0, len(interp)):
    c = ucircle[idx]
    w = np.power(c, z)

    cfunc_plot = dcoloring.colorize(w, grid=False)

    ax.clear()
    ax.imshow(cfunc_plot, extent=(-WIDTH/2, WIDTH/2, -HEIGHT/2, HEIGHT/2))
    ax.set(xlabel='{:3.0f}%'.format(interp[idx] * 100), title='({:5.2f} + {:5.2f}i)^z'.format(np.real(c), np.imag(c)))

    # Save frame
    print('Rendering frame {0:{2}}/{1:{2}}'.format(idx, FRAMES, int(np.log10(FRAMES) + 1)))
    temp_path = '{}/frame.{}.png'.format(TEMP_DIR, idx)
    fig.savefig(temp_path, dpi=600, transparent=True)
    file_names.append(temp_path)

    # Resize for aliasing
    img = cv2.imread(temp_path)
    img = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)), interpolation=cv2.INTER_AREA)
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

render.create_webm(path, file_names, fps=FPS, bitrate='8162k')
rmtree(TEMP_DIR)
plt.close('all')