#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import dcoloring
import cv2

WIDTH = 12
HEIGHT = 24
HEIGHT_OFFSET = 11
POINTS_PER_DIM = 2048

x, y = np.ogrid[
       -WIDTH / 2:WIDTH / 2:POINTS_PER_DIM/2 * 1j,
       HEIGHT_OFFSET + (-HEIGHT / 2):HEIGHT_OFFSET + (HEIGHT / 2):POINTS_PER_DIM * 1j
]

fig = plt.figure()
ax = fig.add_subplot(111)

z = x + 1j * y

z_img = dcoloring.colorize(np.vectorize(dcoloring.zeta)(z, E=1e-9), grid=False)

ax.set(title='f(z)')
ax.imshow(z_img, extent=(
       -WIDTH / 2,
       WIDTH / 2,
       HEIGHT_OFFSET + (-HEIGHT / 2),
       HEIGHT_OFFSET + (HEIGHT / 2)
))

path = 'f(z).png'
fig.savefig(path, dpi=1600, transparent=True)

# Resize for aliasing
img = cv2.imread(path)
img = cv2.resize(img, (int(img.shape[1] / 4), int(img.shape[0] / 4)), interpolation=cv2.INTER_AREA)
cv2.imwrite(path, img)
