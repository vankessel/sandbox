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
FRAMES = 240
FPS = 60
BACK_FORTH = True
TEMP_DIR = 'temp'
OUT_DIR = 'out'

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
    # ('z^i', np.power(z, 1j)),
    # ('z^-i', np.power(z, -1j)),
    ('(1+e^-z)^-1', 1/(1 + np.exp(-z))),
    ('e^(-e^-z)', np.exp(-np.exp(-z))),
    # ('tanh(z)', np.tanh(z)),
    # ('tanh(z^-1)', np.tanh(1/z)),
    ('ln(e^z + 1)', np.log(np.exp(z) + 1))
]

# log_base = np.exp(2*np.pi/6)
for func_name, cfunction in cfunctions:
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
        w = z * (1.0 - interp[idx]) + cfunction * (interp[idx])

        cfunc_plot = dcoloring.colorize(w, grid=False)

        ax.clear()
        ax.imshow(cfunc_plot, extent=(-WIDTH/2, WIDTH/2, -HEIGHT/2, HEIGHT/2))
        ax.set(xlabel='{:3.0f}%'.format(1.0 * 100), title=func_name)

        # Save frame
        print('Rendering frame {0:{2}}/{1:{2}}'.format(idx + 1, FRAMES, int(np.log10(FRAMES) + 1)))
        temp_path = '{}/frame.{}.png'.format(TEMP_DIR, idx)
        fig.savefig(temp_path, dpi=1600, transparent=True)
        file_names.append(temp_path)

        # Resize for aliasing
        img = cv2.imread(temp_path)
        img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(temp_path, img)

        # Save image of complete function
        if idx == len(interp)-1:
            img_path = '{}.png'.format(path)
            fig.savefig(img_path, dpi=1600, transparent=True)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)), interpolation=cv2.INTER_AREA)
            cv2.imwrite('{}.png'.format(path), img)

    if BACK_FORTH:
        file_names = file_names + list(reversed(file_names[1:-1]))

    render.create_webm(path, file_names, fps=FPS, bitrate='8162k')
    rmtree(TEMP_DIR)
    plt.close('all')