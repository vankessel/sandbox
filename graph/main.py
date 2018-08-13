#!/usr/bin/env python

import os
from shutil import rmtree
import matplotlib.pyplot as plt
import numpy as np
import dcoloring, render

WIDTH = 24.0
HEIGHT = 24.0
POINTS_PER_DIM = 1000
FRAMES = 12
TEMP_DIR = 'temp'

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

x, y = np.ogrid[
    -WIDTH/2:WIDTH/2:POINTS_PER_DIM*1j,
    -HEIGHT/2:HEIGHT/2:POINTS_PER_DIM*1j
]
z = x + 1j*y

t = np.arange(0.0, 2*np.pi - 2*np.pi/FRAMES/2, 2*np.pi/FRAMES)
weight1 = dcoloring.clover(   t          )
bias1   = dcoloring.clover(   t, -np.pi/2)
weight2 = dcoloring.clover( 4*t, -np.pi/2)
bias2   = dcoloring.clover( 4*t          )
weight3 = dcoloring.clover(16*t          )
bias3   = dcoloring.clover(16*t, -np.pi/2)

#This loop goes over each weight and bias and generates a plot for each
#These plots are aggregated to make a video showcasing some of the function space

file_names = []
fig = plt.figure()
ax = fig.add_subplot(111)

for idx in range(0, len(t)):
    w = np.exp(weight1[idx] * np.exp(weight2[idx] * np.exp(weight3[idx] * z + bias3[idx]) + bias2[idx]) + bias1[idx])

    img = dcoloring.colorize(w, grid=False)

    ax.clear()
    ax.imshow(img, extent=(-WIDTH/2,WIDTH/2,-HEIGHT/2,HEIGHT/2))
    ax.set_xlim(-WIDTH/2, WIDTH/2)
    ax.set_ylim(-HEIGHT/2, HEIGHT/2)
    ax.set(xlabel='{}'.format(idx))

    print('Rendering frame {0:{2}}/{1:{2}}'.format(idx, FRAMES, int(np.log10(FRAMES)+1)))
    fig.savefig('{}/frame.{}.png'.format(TEMP_DIR, idx))
    file_names.append('{}/frame.{}.png'.format(TEMP_DIR, idx))

render.create_webm('graph', file_names)
rmtree(TEMP_DIR)
