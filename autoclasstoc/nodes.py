"""\
The :mod:`autoclasstoc` module defines two new *docutils* nodes, which make it 
possible to create collapsible content in HTML.
"""

from docutils.nodes import General, Element, TextElement
from sphinx.writers.latex import LaTeXTranslator


class details(General, Element):
    """
    A node that can be expanded or collapsed by the user.

    This is rendered as a ``<details>`` element in HTML.  It is not currently 
    compatible with non-HTML output formats.
    """

    def __init__(self, rawsource='', *children, open_by_default=False, **attributes):
        super().__init__(rawsource, *children, **attributes)
        self['open'] = open_by_default

    def visit_html(visitor, node):
        atts = {
            'class': ' '.join(node['classes'])
        }
        parts = ['details'] + [
            f'{k}="{v}"'
            for k, v in atts.items()
            if v
        ]
        if node['open']:
            parts.append('open')

        visitor.body.append(f"<{' '.join(parts)}>")

    def depart_html(visitor, node):
        visitor.body.append('</details>')

    html = visit_html, depart_html


class details_summary(General, TextElement):
    """
    The summary text to display when a `details` node is collapsed.

    This is rendered as a ``<summary>`` element in HTML.  It is not currently 
    compatible with non-HTML output formats.
    """

    def visit_html(visitor, node):
        visitor.body.append('<summary>')

    def depart_html(visitor, node):
        visitor.body.append('</summary>')

    html = visit_html, depart_html


class AutoClassTocLaTexTranslator(LaTeXTranslator):
    """A custom LaTeX translator that incorporates the `details` and `details_summary` nodes."""

    def visit_details(self, node):
        pass

    def depart_details(self, node):
        pass

    def visit_details_summary(self, node):
        pass

    def depart_details_summary(self, node):
        self.body.append('\n')


def setup(app):
    """
    Configure Sphinx to use the `details` and `details_summary` nodes.
    """
    app.add_node(
        details,
        html=details.html,
    )
    app.add_node(
        details_summary,
        html=details_summary.html,
    )
    app.set_translator('latex', AutoClassTocLaTexTranslator, override=True)
