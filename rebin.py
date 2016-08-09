"""Python/NumPy implementation of IDL's [#fn1]_ rebin function.

.. rubric:: Footnotes

.. [#fn1] http://www.harrisgeospatial.com/docs/rebin.html

"""
import numpy as np

from numpy.lib.stride_tricks import as_strided


def rebin(a, bins, func=None):
    """Aggregate data from the input array `a` into rectangular bins

    The output array results from tiling `a` and applying `func` to each
    tile. `bins` specifies the size of the tiles. More precisely, the
    returned array `out` is such that::

        out[i0, i1, ...] = func(a[b0*i0:b0*(i0+1), b1*i1:b1*(i1+1), ...])

    If `bins` is an integer-like scalar, then ``b0 = b1 = ... = bins``
    in the above formula. If `bins` is a sequence of integer-like
    scalars, then ``b0 = bins[0]``, ``b1 = bins[1]``, ... and the length
    of `bins` must equal the number of dimensions of `a`.

    The reduction function `func` must accept an `axis` argument.
    Examples of such function are

      - ``numpy.mean`` (default),
      - ``numpy.sum``,
      - ``numpy.product``,
      - ...

    The following example shows how a (4, 6) array is reduced to a (2, 2)
    array

    >>> import numpy
    >>> from rebin import rebin
    >>> a = numpy.arange(24).reshape(4, 6)
    >>> rebin(a, bins=(2, 3), func=numpy.sum)
    array([[ 24,  42],
           [ 96, 114]])

    If the elements of `bins` are not integer multiples of the dimensions
    of `a`, the remainding cells are discarded.

    >>> rebin(a, bins=(2, 2), func=numpy.sum)
    array([[16, 24, 32],
           [72, 80, 88]])

    """
    a = np.asarray(a)
    dim = a.ndim
    if np.isscalar(bins):
        bins = dim*(bins,)
    elif len(bins) != dim:
        raise ValueError('length of bins must be {} (was {})'
                         .format(dim, len(bins)))
    if func is None:
        func = np.mean
    for b in bins:
        if b != int(b):
            raise ValueError('bins must be an int or a tuple of ints (was {})'.
                             format(b))

    new_shape = [n//b for n, b in zip(a.shape, bins)]+list(bins)
    new_strides = [s*b for s, b in zip(a.strides, bins)]+list(a.strides)
    aa = as_strided(a, shape=new_shape, strides=new_strides)
    return func(aa, axis=tuple(range(-dim, 0)))
