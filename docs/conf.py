import sys, os
import autoclasstoc

sys.path.append(os.path.dirname(__file__))

project = u'autoclasstoc'
copyright = u'2020, Kale Kundert'
version = autoclasstoc.__version__
release = autoclasstoc.__version__

templates_path = ['_templates']
exclude_patterns = ['_build']
html_static_path = ['_static']
source_suffix = '.rst'
master_doc = 'index'
default_role = 'any'

extensions = [
        '_ext.example',
        '_ext.show_nodes',
        'autoclasstoc',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.viewcode',
        'sphinx.ext.intersphinx',
        'sphinx.ext.napoleon',
        'sphinx_rtd_theme',
]

intersphinx_mapping = {
        'sphinx': ('https://www.sphinx-doc.org/', None),
}
autodoc_default_options = {
        'exclude-members': '__weakref__,__dict__,__module__',
}
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
htmlhelp_basename = 'autoclasstocdoc'
