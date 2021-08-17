import os
import sys

# import sphinxclasstocr

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath(".."))

project = u"sphinxclasstocr"
copyright = u"2020, Kale Kundert"
# version = sphinxclasstocr.__version__
# release = sphinxclasstocr.__version__

templates_path = ["_templates"]
exclude_patterns = ["_build"]
html_static_path = ["_static"]
source_suffix = ".rst"
master_doc = "index"
default_role = "any"

extensions = [
    "_ext.example",
    "_ext.show_nodes",
    "sphinxclasstocr",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "myst_parser",
]

intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/", None),
    "python": ("https://docs.python.org/3.9", None),
    "django": (
        "https://docs.djangoproject.com/en/3.2",
        "https://docs.djangoproject.com/en/3.2/_objects",
    ),
}
autodoc_default_options = {
    "exclude-members": "__weakref__,__dict__,__module__",
}
autosummary_generate = True
pygments_style = "monokai"
pygments_dark_style = "monokai"
html_theme = "furo"

# The name of the Pygments (syntax highlighting) style to use.
# Available styles ['default', 'emacs', 'friendly', 'colorful',
# 'autumn', 'murphy', 'manni', 'material', 'monokai', 'perldoc',
# 'pastie', 'borland', 'trac', 'native', 'fruity', 'bw', 'vim',
# 'vs', 'tango', 'rrt', 'xcode', 'igor', 'paraiso-light', 'paraiso-dark',
# 'lovelace', 'algol', 'algol_nu', 'arduino', 'rainbow_dash', 'abap',
# 'solarized-dark', 'solarized-light', 'sas', 'stata', 'stata-light',
# 'stata-dark', 'inkpot', 'zenburn', 'gruvbox-dark', 'gruvbox-light']
pygments_style = "monokai"
pygments_dark_style = "monokai"


def setup(app):
    app.add_css_file("css/sphinxclasstocr.css")
