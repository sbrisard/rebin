# -*- coding: utf-8 -*-
import re

from setuptools import setup


with open('rebin.py', 'r') as f:
    lines = f.read()
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        lines, re.MULTILINE).group(1)
    description = re.search(r'^\"\"\"(.*)', lines, re.MULTILINE).group(1)

setup(
    name='rebin',
    version=version,
    description=description,
    url='https://github.com/sbrisard/rebin',
    author='Sébastien Brisard',
    author_email='',
    py_modules=['rebin'],
    license='BSD-3',
)
