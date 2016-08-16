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
    description = re.search(r'^u\"\"\"(.*)',
                            lines, re.MULTILINE).group(1)
    long_description = re.search('^u\"\"\"(.*)^\"\"\"',
                                 lines, re.MULTILINE | re.DOTALL).group(1)
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]',
                       lines, re.MULTILINE).group(1)

print(long_description)

setup(
    name='rebin',
    version=version,
    description=description,
    long_description=long_description,
    url='https://github.com/sbrisard/rebin',
    author=author,
    author_email='',
    py_modules=['rebin'],
    license='BSD-3',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Topic :: Software Development :: Build Tools',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering'],
    test_suite='setup.my_test_suite',
    install_requires=['numpy'],
)
