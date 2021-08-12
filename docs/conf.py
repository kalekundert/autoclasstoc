import os
import sys

# import sphinxclasstocr

sys.path.append(os.path.dirname(__file__))

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
}
autodoc_default_options = {
    "exclude-members": "__weakref__,__dict__,__module__",
}
autosummary_generate = True
pygments_style = "monokai"
pygments_dark_style = "monokai"
html_theme = "sphinx_rtd_theme"


def setup(app):
    app.add_css_file("css/sphinxclasstocr.css")
