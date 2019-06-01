import numpy as np
from colorsys import hls_to_rgb


# Domain coloring function
def colorize(z, max_sat=0.9, grid_taper=0.02, log_base=2.0, grid=True):
    r = np.abs(z)
    arg = np.angle(z)
    real = np.real(z)
    imag = np.imag(z)

    if grid:
        height = np.sqrt(max_sat)
        real_subpos = real - np.floor(real)
        real_sat = plateau_curve(real_subpos, grid_taper, height)

        imag_subpos = imag - np.floor(imag)
        imag_sat = plateau_curve(imag_subpos, grid_taper, height)

        s = real_sat * imag_sat
    else:
        s = max_sat

    log2r = np.log2(r)
    if log_base != 2.0:
        log2r /= np.log2(log_base)

    h = arg / (2 * np.pi)
    l = (log2r - np.floor(log2r)) / 5 + 2 / 5

    c = np.vectorize(hls_to_rgb)(h, l, s)
    c = np.array(c).swapaxes(0, 2)
    c = np.flip(c, 0)
    return c


def cos_interpolation(x):
    return (1 - np.cos(np.pi * x)) / 2


def plateau_curve(x, taper_length=0.05, height=1.0, total_length=1.0):
    conditions = [
        x < taper_length,
        np.logical_and(taper_length <= x, x <= total_length - taper_length),
        total_length - taper_length < x
    ]
    functions = [
        lambda x: height * cos_interpolation(x / taper_length),
        lambda x: height,
        lambda x: height * cos_interpolation((total_length - x) / taper_length)
    ]
    return np.piecewise(x, conditions, functions)


def clover(theta, offset=0.0):
    return np.cos(2 * theta + offset) * np.exp(theta * 1j)
