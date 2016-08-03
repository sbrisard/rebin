import unittest

import numpy as np

from numpy.testing import assert_array_almost_equal_nulp
from numpy.testing import assert_array_equal

from rebin import rebin


def my_rebin(a, bins, func=np.mean):
    new_shape = tuple(n // b for n, b in zip(a.shape, bins))
    bin0, bin1 = bins

    def compute_cell(i0, i1):
        return func(a[bin0*i0:bin0*(i0+1), bin1*i1:bin1*(i1+1)])

    out = np.empty(new_shape, dtype=a.dtype)
    it = np.nditer(out, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        it.value[...] = compute_cell(*it.multi_index)
        it.iternext()
    return out


class TestInvalidParameters(unittest.TestCase):
    def test_invalid_length_of_bins(self):
        a = np.array([[1., 2., 3.],
                      [4., 5., 6.]])
        with self.assertRaises(ValueError):
            rebin(a, bins=(1, 2, 3))


class TestBasic(unittest.TestCase):
    def test1(self):
        a = np.linspace(1, 24, num=24,
                        dtype=np.float64).reshape(4, 6)
        actual = rebin(a, (2, 3))
        expected = np.array([[5., 8.],
                             [17., 20.]])
        assert_array_equal(expected, actual)

    def test2(self):
        a = np.linspace(1, 24, num=24,
                        dtype=np.float64).reshape(4, 6)
        actual = rebin(a, 2)
        expected = np.array([[4.5, 6.5, 8.5],
                             [16.5, 18.5, 20.5]])
        assert_array_equal(expected, actual)


class TestRandomData(unittest.TestCase):
    def setUp(self):
        np.random.seed(20160711)

    def test1(self):
        shape = (24, 18)
        bins = (4, 3)
        a = 2*np.random.rand(*shape)-1
        actual = rebin(a, bins, np.sum)
        expected = my_rebin(a, bins, np.sum)
        assert_array_almost_equal_nulp(expected, actual, nulp=3)


if __name__ == '__main__':
    unittest.main()
