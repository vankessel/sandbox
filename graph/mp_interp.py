#!/usr/bin/env python

import os
from shutil import rmtree
import matplotlib.pyplot as plt
import numpy as np
import cv2
import dcoloring, render
from multiprocessing import Pool

FILE_NAME = 'exp(z)'
WIDTH = 1.5
HEIGHT = 1.5
POINTS_PER_DIM = 2048
FRAMES = 240
FPS = 60
BACK_FORTH = True
TEMP_DIR = 'temp'
OUT_DIR = 'mp_out'

x, y = np.ogrid[
    -WIDTH/2:WIDTH/2:POINTS_PER_DIM*1j,
    -HEIGHT/2:HEIGHT/2:POINTS_PER_DIM*1j
]
z = x + 1j*y

# 0 to 1 inclusive
lerp = np.arange(0.0, 1.0 + 1.0/FRAMES/2, 1.0/FRAMES)
cerp = dcoloring.cos_interpolation(lerp)
interp = cerp

# Perpare plots and function
func_name = 'tan(z^-1)'
path = OUT_DIR + '/' + func_name

def save_frame(idx):

    w = z * (1.0 - interp[idx]) + np.tan(1/z) * (interp[idx])

    cfunc_plot = dcoloring.colorize(w, grid=False)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.imshow(cfunc_plot, extent=(-WIDTH / 2, WIDTH / 2, -HEIGHT / 2, HEIGHT / 2))
    ax.set(xlabel='{:3.0f}%'.format(interp[idx] * 100), title=func_name)

    # Save frame
    print('Rendering frame {0:{2}}/{1:{2}}'.format(idx, FRAMES, int(np.log10(FRAMES) + 1)))
    temp_path = '{}/frame.{}.png'.format(TEMP_DIR, idx)
    fig.savefig(temp_path, dpi=600, transparent=True)

    # Resize for aliasing
    img = cv2.imread(temp_path)
    img = cv2.resize(img, (int(img.shape[1] / 3), int(img.shape[0] / 3)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(temp_path, img)

    # Save image of complete function
    if idx == FRAMES - 1:
        img_path = '{}.png'.format(path)
        fig.savefig(img_path, dpi=1600, transparent=True)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (int(img.shape[1] / 4), int(img.shape[0] / 4)), interpolation=cv2.INTER_AREA)
        cv2.imwrite('{}.png'.format(path), img)

    plt.close(fig)


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
    # ('Zoomed sin(z^-1)2', np.sin(1/z)),
    # ('Area_6-3_8m', np.tan(1/z)),
]

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

print('Processing {}'.format(func_name))

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

with Pool(processes=3) as pool:
    pool.map(save_frame, range(0, len(interp)))

file_paths = sorted(['{}/{}'.format(TEMP_DIR, fn) for fn in os.listdir(TEMP_DIR)], key=lambda fp: int(fp.split('.')[1]))

if BACK_FORTH:
    file_paths = file_paths + list(reversed(file_paths[1:-1]))

render.create_webm(path, file_paths, fps=FPS, bitrate='8162k')
rmtree(TEMP_DIR)
plt.close('all')
