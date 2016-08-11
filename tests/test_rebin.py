import unittest

import numpy as np

from numpy.testing import assert_array_almost_equal_nulp
from numpy.testing import assert_array_equal

from rebin import rebin


def my_rebin(a, factor, func=np.mean):
    new_shape = tuple(n // f for n, f in zip(a.shape, factor))

    def compute_cell(indices):
        slices = tuple(slice(f*i, f*(i+1)) for f, i in zip(factor, indices))
        return func(a[slices])

    # Find out what the type of the output will be
    dummy = compute_cell(a.ndim*(0,))
    out = np.empty(new_shape, dtype=dummy.dtype)
    it = np.nditer(out, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        it.value[...] = compute_cell(it.multi_index)
        it.iternext()
    return out


class TestInvalidParameters(unittest.TestCase):
    def setUp(self):
        self.a = np.array([[1., 2., 3.],
                           [4., 5., 6.]])

    def test_invalid_length_of_factor(self):
        with self.assertRaises(ValueError):
            rebin(self.a, factor=(1, 2, 3))

    def test_factor_not_tuple_of_ints(self):
        with self.assertRaises(ValueError):
            rebin(self.a, factor=(2, 1.5))

    def test_factor_not_int(self):
        with self.assertRaises(ValueError):
            rebin(self.a, factor=1.5)


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


class TestRandomFloats(unittest.TestCase):
    def setUp(self):
        np.random.seed(20160711)

    def do_test(self, shape, factor, func=None, nulp=1):
        a = 2*np.random.rand(*shape)-1
        actual = rebin(a, factor, np.sum)
        expected = my_rebin(a, factor, np.sum)
        assert_array_almost_equal_nulp(expected, actual, nulp=nulp)

    def test1(self):
        self.do_test((24, 18), (4, 3), nulp=3)

    def test2(self):
        self.do_test((4, 6, 8), (2, 3, 4), nulp=4)


class TestRandomInts(unittest.TestCase):
    def setUp(self):
        np.random.seed(20160804)

    def do_test(self, shape, factor, func=None):
        a = 2*np.random.randint(-1000, 1000, shape)
        actual = rebin(a, factor, np.sum)
        expected = my_rebin(a, factor, np.sum)
        assert_array_equal(expected, actual)

    def test1(self):
        self.do_test((24, 18), (4, 3))

    def test2(self):
        self.do_test((4, 6, 8), (2, 3, 4))


class TestInexactDivision(unittest.TestCase):
    """Assert that remainding cells are discarded."""

    def test1(self):
        a = np.arange(56).reshape(7, 8)
        actual = rebin(a, factor=(2, 3), func=np.sum)
        expected = np.array([[30, 48],
                             [126, 144],
                             [222, 240]])
        assert_array_equal(expected, actual)

if __name__ == '__main__':
    unittest.main()
