#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import dcoloring
import cv2

WIDTH = 16.0
HEIGHT = 16.0
POINTS_PER_DIM = 2048

x, y = np.ogrid[
    -WIDTH/2:WIDTH/2:POINTS_PER_DIM*1j,
    -HEIGHT/2:HEIGHT/2:POINTS_PER_DIM*1j
]

fig = plt.figure()
ax = fig.add_subplot(111)

z = x + 1j*y

z_img = dcoloring.colorize(z, grid=False)

ax.set(title='z')
ax.imshow(z_img, extent=(-WIDTH/2,WIDTH/2,-HEIGHT/2,HEIGHT/2))

path  = 'z.png'
fig.savefig(path, dpi=1600, transparent=True)

# Resize for aliasing
img = cv2.imread(path)
img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)), interpolation=cv2.INTER_AREA)
cv2.imwrite(path, img)
