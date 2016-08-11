#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import datetime
import os

import rebin

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = 'rebin'
author = rebin.__author__

initial_year = 2016
today = datetime.date.today()
current_year = today.year
if current_year == initial_year:
    copyright = '{}, {}. BSD-3 license'.format(initial_year, author)
else:
    copyright = '2016-{}, {}. BSD-3 license'.format(initial_year,
                                                    current_year,
                                                    author)

version = rebin.__version__
release = rebin.__release__

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
   author, 'manual'),
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
