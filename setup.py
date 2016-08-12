# -*- coding: utf-8 -*-
import re
import unittest

from setuptools import setup


def my_test_suite():
    """From http://stackoverflow.com/questions/17001010/.

    """
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


with open('rebin.py', 'r') as f:
    lines = f.read()
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        lines, re.MULTILINE).group(1)
    description = re.search(r'^\"\"\"(.*)',
                            lines, re.MULTILINE).group(1)
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]',
                       lines, re.MULTILINE).group(1)

setup(
    name='rebin',
    version=version,
    description=description,
    url='https://github.com/sbrisard/rebin',
    author=author,
    author_email='',
    py_modules=['rebin'],
    license='BSD-3',
    test_suite='setup.my_test_suite',
    install_requires=['numpy'],
)
