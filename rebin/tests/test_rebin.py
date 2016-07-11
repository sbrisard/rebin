import unittest

import numpy as np
import numpy.testing as nptesting

from rebin import rebin


class TestRebin(unittest.TestCase):
    def setUp(self):
        np.random.seed(20160711)

    def test_rebin(self):
        shape = (24, 18)
        a = 2*np.random.rand(24, 18)-1
        bin_shape = (4, 3)
        actual = rebin(a, bin_shape)
        n0, n1 = (i//j for i, j in zip(shape, bin_shape))
        bin0, bin1 = bin_shape
        expected = np.zeros((n0, n1), dtype=np.float64)
        for i0 in range(n0):
            for i1 in range(n1):
                for j0 in range(bin0):
                    for j1 in range(bin1):
                        expected[i0, i1] += a[bin0*i0+j0, bin1*i1+j1]
        nptesting.assert_array_equal(expected, actual)


if __name__ == '__main__':
    unittest.main()
