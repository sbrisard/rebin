import numpy as np

from numpy.lib.stride_tricks import as_strided


def rebin(a, bins, func=np.mean):
    dim = a.ndim
    if np.isscalar(bins):
        bins = dim*(bins,)
    elif len(bins) != dim:
        raise ValueError('length of bins must be {} (was {})'
                         .format(dim, len(bins)))

    new_shape = [n//b for n, b in zip(a.shape, bins)]+list(bins)
    new_strides = [s*b for s, b in zip(a.strides, bins)]+list(a.strides)
    aa = as_strided(a, shape=new_shape, strides=new_strides)
    return func(aa, axis=tuple(range(-dim, 0)))
