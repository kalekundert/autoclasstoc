#!/usr/bin/env python3

from docutils import nodes
from docutils.parsers.rst import Directive

class ShowNodesDirective(Directive):
    """
    Pretty print all the nodes in the restructured-text contained in this 
    directive.  This is only meant to be a tool for developing and debugging 
    new Sphinx extensions.

    Example:

        .. show-nodes::

            .. figure:: path/to/image.png

                Caption...
    """
    has_content = True

    def run(self):
        wrapper = nodes.paragraph()
        self.state.nested_parse(self.content, self.content_offset, wrapper)

        for node in wrapper.children:
            print(node.pformat())

        return wrapper.children


def setup(app):
    app.add_directive('shownodes', ShowNodesDirective)
