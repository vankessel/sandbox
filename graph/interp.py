#!/usr/bin/env python

import os
from shutil import rmtree
import matplotlib.pyplot as plt
import numpy as np
import dcoloring, render

WIDTH = 16.0
HEIGHT = 16.0
POINTS_PER_DIM = 512
FRAMES = 60
FPS = 12
BACK_FORTH = True
TEMP_DIR = 'temp'

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

x, y = np.ogrid[
    -WIDTH/2:WIDTH/2:POINTS_PER_DIM*1j,
    -HEIGHT/2:HEIGHT/2:POINTS_PER_DIM*1j
]
z = x + 1j*y

lerp = np.arange(0.0, 1.0 + 1.0/FRAMES/2, 1.0/FRAMES)
cerp = dcoloring.cos_interpolation(lerp)

#Animate transistion between two complex functions

file_names = []
fig = plt.figure()
ax = fig.add_subplot(111)

interp = cerp
for idx in range(0, len(interp)):
    w = z * (1.0 - interp[idx]) + 1/(z*z*z) * (interp[idx])

    img = dcoloring.colorize(w, grid=False)

    ax.clear()
    ax.imshow(img, extent=(-WIDTH/2,WIDTH/2,-HEIGHT/2,HEIGHT/2))
    ax.set_xlim(-WIDTH/2, WIDTH/2)
    ax.set_ylim(-HEIGHT/2, HEIGHT/2)
    ax.set(xlabel='{}'.format(idx))

    print('Rendering frame {0:{2}}/{1:{2}}'.format(idx, FRAMES, int(np.log10(FRAMES)+1)))
    fig.savefig('{}/frame.{}.png'.format(TEMP_DIR, idx))
    file_names.append('{}/frame.{}.png'.format(TEMP_DIR, idx))

if BACK_FORTH:
    file_names = file_names + list(reversed(file_names[1:-1]))

render.create_webm('graph', file_names)
rmtree(TEMP_DIR)
