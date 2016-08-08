"""Python/NumPy implementation of IDL's rebin function.

"""
import numpy as np

from numpy.lib.stride_tricks import as_strided


def rebin(a, bins, func=np.mean):
    """Aggregate data from the input array `a` into rectangular bins

    The output array results from tiling `a` and applying `func` to each
    tile. `bins` specifies the size of the tiles.

    More precisely, the returned array `out` is such that

        out[i0, i1, ...] = func(a[b0*i0:b0*(i0+1), b1*i1:b1*(i1+1), ...])

    If `bins` is an integer-like scalar, then ``b0 = b1 = ... = bins``
    in the above formula. If `bins` is a sequence of integer-like
    scalars, then ``bins = (b0, b1, ...)`` and the length of `bins`
    must equal the number of dimensions of `a`.

    """
    a = np.asarray(a)
    dim = a.ndim
    if np.isscalar(bins):
        bins = dim*(bins,)
    elif len(bins) != dim:
        raise ValueError('length of bins must be {} (was {})'
                         .format(dim, len(bins)))
    for b in bins:
        if b != int(b):
            raise ValueError('bins must be an int or a tuple of ints (was {})'.
                             format(b))

    new_shape = [n//b for n, b in zip(a.shape, bins)]+list(bins)
    new_strides = [s*b for s, b in zip(a.strides, bins)]+list(a.strides)
    aa = as_strided(a, shape=new_shape, strides=new_strides)
    return func(aa, axis=tuple(range(-dim, 0)))
