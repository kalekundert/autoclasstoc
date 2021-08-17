import os
import sys

# import sphinxclasstocr

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath(".."))

project = u"sphinxclasstocr"
copyright = u"2020, Kale Kundert"
# version = sphinxclasstocr.__version__
# release = sphinxclasstocr.__version__

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
    "sphinx_copybutton",
]

default_role = "any"
exclude_patterns = ["_build"]
html_static_path = ["_static"]
html_theme = "furo"
master_doc = "index"
source_suffix = ".rst"
templates_path = ["_templates"]

intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/", None),
    "python": ("https://docs.python.org/3.9", None),
    "django": (
        "https://docs.djangoproject.com/en/3.2",
        "https://docs.djangoproject.com/en/3.2/_objects",
    ),
}

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

# -- Options for extensions configuration ------------------------------------

# sphinx-copybutton is a lightweight code-block copy button
# config options are here https://sphinx-copybutton.readthedocs.io/en/latest/
# This config removes Python Repl + continuation, Bash line prefixes,
# ipython and qtconsole + continuation, jupyter-console + continuation and preceding line numbers
copybutton_prompt_text = (
    r"^\d|^.\d|^\d\d|^\d\d\d|>>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
)
copybutton_prompt_is_regexp = True

# datalad download-url http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf \
# --dataset . \
# -m "add beginners guide on bash" \
# -O books/bash_guide.pdf
# is correctly pasted with the following setting
copybutton_line_continuation_character = "\\"


autodoc_default_options = {
    "exclude-members": "__weakref__,__dict__,__module__",
}
autosummary_generate = True


def setup(app):
    app.add_css_file("css/sphinxclasstocr.css")
