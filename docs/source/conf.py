#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys
import os
import shlex

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = 'rebin'
copyright = '2016, Sébastien Brisard'
author = 'Sébastien Brisard'
version = '0.1'
release = '0.1'

language = None

exclude_patterns = []

pygments_style = 'sphinx'

todo_include_todos = False

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
html_domain_indices = False
html_use_index = False
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
html_use_opensearch = ''
htmlhelp_basename = 'rebindoc'

latex_elements = {}
latex_documents = [
  (master_doc, 'rebin.tex', 'Rebin Documentation',
   'Sébastien Brisard', 'manual'),
]

man_pages = [
    (master_doc, 'rebin', 'Rebin Documentation',
     [author], 1)
]

texinfo_documents = [
  (master_doc, 'rebin', 'Rebin Documentation',
   author, 'rebin',
   "Python/NumPy implementation of IDL's rebin function.",
   'Miscellaneous'),
]

if on_rtd:
    from unittest.mock import MagicMock

    class Mock(MagicMock):
        @classmethod
        def __getattr__(cls, name):
            return Mock()

    MOCK_MODULES = ['numpy', 'numpy.lib.stride_tricks']
    sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)
