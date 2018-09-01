#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import dcoloring

WIDTH = 24.0
HEIGHT = 24.0
POINTS_PER_DIM = 2048

x, y = np.ogrid[
    -WIDTH/2:WIDTH/2:POINTS_PER_DIM*1j,
    -HEIGHT/2:HEIGHT/2:POINTS_PER_DIM*1j
]

fig = plt.figure()
axes = []
axes.append(fig.add_subplot(121))
axes.append(fig.add_subplot(122, sharex=axes[0], sharey=axes[0]))

z = x + 1j*y
w = np.log(1/z)

z_img = dcoloring.colorize(z, grid=False)
w_img = dcoloring.colorize(w, grid=False)

axes[0].set(title='z')
axes[0].imshow(z_img, extent=(-WIDTH/2,WIDTH/2,-HEIGHT/2,HEIGHT/2))
axes[1].set(title='w')
axes[1].imshow(w_img, extent=(-WIDTH/2,WIDTH/2,-HEIGHT/2,HEIGHT/2))

for ax in axes:
    ax.set_xlim(-WIDTH/2, WIDTH/2)
    ax.set_ylim(-HEIGHT/2, HEIGHT/2)

plt.show()
