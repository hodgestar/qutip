#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import pathlib
import warnings

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '1.8.3'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.mathjax',
              'matplotlib.sphinxext.plot_directive',
              'sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.doctest',
              'sphinx.ext.autosummary',
              'numpydoc',
              'sphinx.ext.extlinks',
              'sphinx.ext.viewcode',
              'sphinx.ext.ifconfig',
              'sphinx.ext.napoleon',
              'sphinx_gallery.gen_gallery',
              'sphinxcontrib.bibtex']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# This is needed for ipython @savefig
# Otherwise it just puts the png in the root dir
savefig_dir = '_images'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'QuTiP: Quantum Toolbox in Python'
author = ', '.join([
    'P.D. Nation',
    'J.R. Johansson',
    'A.J.G. Pitchford',
    'C. Granade',
    'A.L. Grimsmo',
    'N. Shammah',
    'S. Ahmed',
    'N. Lambert',
    'B. Li',
    'J. Lishman',
    'S. Cross',
    'and E. Giguère'
])

copyright = '2011 to 2021 inclusive, QuTiP developers and contributors'


def _check_source_folder_and_imported_qutip_match():
    """ Warn if the imported qutip and the source folder the documentation
        is being built from don't match.

        The generated documentation contains material from both the
        source folder (e.g. ``.rst`` files) and from the imported qutip
        (e.g. docstrings), so if the two don't match the generated
        documentation will be a chimera.
    """
    import qutip
    qutip_folder = pathlib.Path(qutip.__file__).absolute().parent.parent
    source_folder = pathlib.Path(__file__).absolute().parent.parent
    if qutip_folder != source_folder:
        warnings.warn(
            "The documentation source and imported qutip package are"
            " not from the same source folder. This may result in the"
            " documentation containing text from different sources."
            " Documentation source: {!r}."
            " Qutip package source: {!r}.".format(
                str(source_folder), str(qutip_folder)
            )
        )


_check_source_folder_and_imported_qutip_match()


def qutip_version():
    """ Retrieve the QuTiP version from ``../VERSION``.
    """
    src_folder_root = pathlib.Path(__file__).absolute().parent.parent
    version = src_folder_root.joinpath(
        "VERSION"
    ).read_text().strip()
    return version


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# The full version, including alpha/beta/rc tags.
release = qutip_version()
# The short X.Y version.
version = ".".join(release.split(".")[:2])
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'gallery/src',  # handled by sphinx-gallery instead.
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []
todo_include_todos = True

numpydoc_show_class_members = False
napoleon_numpy_docstring = True
napoleon_use_admonition_for_notes = True

# sphinxcontrib.bixtex options
bibtex_bibfiles = [
    "guide/heom/heom.bib",
]

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
full_logo= True


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
}
# Add any paths that contain custom themes here, relative to this directory.

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = 'QuTiP {} Documentation'.format(version)

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = 'QuTiP'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'figures/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {'sidebar': ['localtoc.html', 'sourcelink.html', 'searchbox.html']}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

html_css_files = [
    'site.css',
]

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'QuTiPdoc'


# -- Configure MathJax for maths output in HTML targets

# Currently (2021-04-10) Sphinx 3.5.3 loads MathJax 2.7, which does not have
# support for the 'physics' package.  MathJax 3 does, so once Sphinx is using
# that (should be in Sphinx 4), you will be able to swap to using that.  In the
# meantime, we just have to define all the functions we're going to use.
#
# See:
# - https://docs.mathjax.org/en/v3.0-latest/input/tex/extensions/physics.html
mathjax3_config = {
    'TeX': {
        'Macros': {
            'bra': [r'\left\langle{#1}\right\rvert', 1],
            'ket': [r'\left\lvert{#1}\right\rangle', 1],
            'tr': r'\operatorname{tr}',
        },
    },
}

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'classoptions': '',
    'babel': '\\usepackage[english]{babel}',
    'fncychap': '',
    'figure_align': 'H',
    'maxlistdepth': '10', #added this line
    # This preamble is inserted into the build tools for the latex make targets
    # but not any others.  Be sure to change mathjax_config too if you need to
    # define more commands.
    'preamble': r"\usepackage{physics}",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'qutip.tex', project, author, 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = 'figures/logo.png'

# Sometimes make might suggest setting this to False.
# It screws a few things up if you do - don't be tempted.
latex_keep_old_macro_names=True

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = True

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'qutip', project, [author], 1)
]

# -- Doctest Setup ---------------------------------------

os_nt = False
if os.name == "nt":
    os_nt = True

doctest_global_setup = '''
import matplotlib.pyplot as plt
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")
from qutip import *
os_nt = {}
'''.format(os_nt)

# -- Options for plot directive ---------------------------------------

plot_working_directory = "./"
plot_pre_code = """
import numpy as np
import matplotlib.pyplot as plt
from qutip import *
plt.close("all")
"""
plot_include_source = True
plot_html_show_source_link = False
plot_html_show_formats = False

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'qutip', project,
     author, 'QuTiP',
     'Quantum Toolbox in Python',
     'Miscellaneous'),
]

autodoc_member_order = 'alphabetical'

## EXTLINKS CONFIGURATION ######################################################

extlinks = {
    'arxiv': ('https://arxiv.org/abs/%s', 'arXiv:%s'),
    'doi': ('https://dx.doi.org/%s', 'doi:%s'),
}

# configuration declares the location of the examples directory for
# Sphinx Gallery

sphinx_gallery_conf = {
     'examples_dirs': 'gallery/src',   # path to your example scripts
     'gallery_dirs': 'gallery/build',  # save generated examples
     'abort_on_example_error': True  # abort if exception occurs
}

ipython_strict_fail = False
