#!/usr/bin/env python3

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import ReferenceRole
from autoclasstoc import utils

class Example(Directive):
    has_content = True

    def run(self):
        wrapper = nodes.paragraph()
        wrapper += utils.nodes_from_rst(self.state, [
                '.. code-block:: rst',
                '',
                *['    ' + x for x in self.content],
        ])
        wrapper += utils.nodes_from_rst(self.state, self.content)
        return wrapper.children

class SphinxExtRole(ReferenceRole):

    def run(self):
        title = f'sphinx.ext.{self.text}'
        url = f'https://www.sphinx-doc.org/en/master/usage/extensions/{self.text}.html'
        a = nodes.reference('', '', internal=False, refuri=url)
        a += nodes.literal(title, title)
        return [a], []

def setup(app):
    app.add_directive('example', Example)
    app.add_role('ext', SphinxExtRole())
    app.add_object_type(
            'confval',
            'confval',
            objname='configuration value',
            indextemplate='pair: %s; configuration value',
    )



