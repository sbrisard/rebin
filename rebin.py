"""Python/NumPy implementation of IDL's rebin function.

See http://www.harrisgeospatial.com/docs/rebin.html.

The ``rebin`` function defined in this module first groups the cells of
the input array in tiles of specified size. Then, a reduction function
is applied to each tile, which is replaced by a single value. The
resulting array is returned: its dimensions are the number of tiles in
the input array.

Rationale
=========

The input array, ``a`` is assumed to be *strided*. In other words, if ::

    a.strides = (s0, s1, ...),

then ::

    a[i0, i1, ...] = a[[s0*i0 + s1*i1 + ...]],

where ``[[...]]`` denotes the offset operator. To compute the output
array, we first create a tiled version of ``a``. The number of
dimensions of ``tiled`` is twice that of ``a``: for each index in ``a``,
``tiled`` has one *slow* index and one *fast* index ::

    tiled[i0, i1, ..., j0, j1, ...] = a[b0*i0 + j0, b1*i1 + j1, ...].

Upon using the strides of ``a`` ::

    tiled[i0, i1, ..., j0, j1, ...] = a[[s0*b0*i0 + s1*b1*i1 + ... +
                                         s0*j0 + s1*j1 + ...]],

which shows that the strides of ``tiled`` are ::

    tiled.strides = (s0*b0, s1*b1, ..., s0, s1, ...).

In other words, ``tiled`` is a *view* of ``a`` with modified strides.
Restriding an array can be done with the ``as_strided`` function from
``numpy.lib.stride_tricks``. Then, the output array is readily computed
as follows ::

    out = func(tiled, axis = tuple(range(-a.ndim, 0)))

where reduction is carried out on the fast indices.

Boundary cases
==============

When the dimensions of the input array are not integer multiples of the
dimensions of the tiles, the remainding rows/columns are simply discarded.
For example ::

    +--------+--------+--------+--------+----+
    |  1   1 |  2   2 |  3   3 |  4   4 |  5 |
    |  1   1 |  2   2 |  3   3 |  4   4 |  5 |
    +--------+--------+--------+--------+----+
    |  6   6 |  7   7 |  8   8 |  9   9 | 10 |
    |  6   6 |  7   7 |  8   8 |  9   9 | 10 |
    +--------+--------+--------+--------+----+
    | 11  11 | 12  12 | 13  13 | 14  14 | 15 |
    +--------+--------+--------+--------+----+

will produce ::

    +----+----+----+----+
    |  4 |  8 | 12 | 16 |
    +----+----+----+----+
    | 24 | 28 | 32 | 36 |
    +----+----+----+----+

for (2, 2) tiles and a *sum* reduction.

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
