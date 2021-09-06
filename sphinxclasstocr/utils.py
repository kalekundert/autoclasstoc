#!/usr/bin/env python3

"""A group of functions to build sphinxclastocr groups.
"""

import inspect
from importlib import import_module

from docutils import nodes as _nodes
from docutils.statemachine import StringList, string2lines
from sphinx.util.docstrings import extract_metadata

from .errors import ConfigError
from .nodes import Details, DetailsSummary
from .sections import SECTIONS, Section


def pick_class(qual_name, env):
    """Figure out which class to make the TOC for.

    We can either be given this information as an argument, or we can try to
    figure it out from the context (e.g. the :rst:dir:`sphinxclasstocr` or
    :rst:dir:`py:class` currently being processed).

    Arguments:
        qual_name (str): The name of the class to pick, or None if the class
            should be inferred from the environment.
        env (sphinx.environment.BuildEnvironment): This object is available as
            :attr:`self.env` from :class:`~sphinx.util.docutils.SphinxDirective`
            subclasses.
    """
    if qual_name:
        mod_name, cls_name = qual_name.rsplit(".", 1)
    else:
        cls_name = env.temp_data.get("autodoc:class") or env.ref_context.get(
            "py:class"
        )
        mod_name = env.temp_data.get("autodoc:module") or env.ref_context.get(
            "py:module"
        )

        if not cls_name:
            raise ConfigError("no class name")
        if not mod_name:
            raise ConfigError("no module name")

    return mod_name, cls_name


def load_class(mod_name, cls_name):
    """Import the given class from the given module."""
    mod = import_module(mod_name)
    cls = getattr(mod, cls_name)
    return mod, cls


def pick_sections(sections, exclude=None):
    """Determine which sections to include in the class TOC.

    The return value will be a list in the same order as *sections*, but with
    any sections from *exclude* removed.  Both arguments can specify sections
    using string names (e.g. "public-methods") or un-instantiated `Section`
    classes.  All names will be converted to classes in the return value.
    """

    def _section_from_anything(anything):
        # from .sections import SECTIONS, Section

        if isinstance(anything, str):
            try:
                return SECTIONS[anything]
            except KeyError as key_error:
                raise ConfigError(
                    f"no sphinxclasstocr section with key {anything!r}"
                ) from key_error

        if inspect.isclass(anything) and issubclass(anything, Section):
            return anything

        raise ConfigError(
            f"Must be type(sphinxclasstocr.Section), type({str(type(anything))}) was supplied"
        )

    sections = [_section_from_anything(anything) for anything in sections]
    exclude = {_section_from_anything(anything) for anything in exclude or []}
    return [x for x in sections if x not in exclude]


def make_toc(state, cls, sections):
    """Create the class TOC."""
    _toc = []
    for section_cls in sections:
        section = section_cls(state, cls)
        section.check()
        _toc += section.format()

    _toc.append(_nodes.transition())
    return _toc


def make_container():
    """
    Make a container node to identify elements associated with the
    :rst:dir:`sphinxclasstocr` directive.
    """
    return _nodes.container(classes=["sphinxclasstocr"])


def make_rubric(title):
    """Make an informal header."""
    return _nodes.rubric(title, title)


def make_inherited_details(state, parent, open_by_default=False):
    """
    Make a collapsible node to contain information about inherited
    attributes.
    """

    _details_summary = DetailsSummary()
    _details_summary += strip_p(
        nodes_from_rst(
            state, f"Inherited from :py:class:`{parent.__qualname__}`"
        )
    )

    _details = Details(open_by_default)
    _details += _details_summary
    return _details


def make_links(state, attrs):
    """Make links to the given class attributes.

    More specifically, the links are made using the :rst:dir:`autosummary`
    directive.
    """
    assert attrs
    return nodes_from_rst(
        state,
        [
            ".. autosummary::",
            "",
            *[f"    {x}" for x in attrs],
        ],
    )


def find_inherited_attrs(cls):
    """
    Return a dictionary mapping parent classes to the attributes inherited from
    those classes.
    """
    return {
        base: base.__dict__
        for base in cls.__mro__
        if base not in (cls, object)
    }


def filter_attrs(attrs, predicate):
    """
    Remove attributes for which the given predicate function returns False.
    """

    return {
        k: v
        for k, v in attrs.items()
        if predicate(k, v, extract_metadata(inspect.getdoc(v)))
    }


def nodes_from_rst(state, rst):
    """Create nodes from the given restructured text.

    The *rst* argument can either be any of the following types:

    - string, with any number of lines
    - list of strings
    - StringList (the type used by docutils to represent lines of restructured
      text)
    - node
    """
    if isinstance(rst, str):
        rst = string2lines(rst)
    if isinstance(rst, list):
        rst = StringList(rst)
    if isinstance(rst, _nodes.Node):
        return rst

    wrapper = _nodes.paragraph()
    state.nested_parse(rst, 0, wrapper)
    return wrapper.children


def strip_p(nodes):
    """Remove any top-level paragraph nodes.

    Parsing a simple string like "Hello world" with `nodes_from_rst` will
    return text wrapped in a paragraph.  If this paragraph is not desired (e.g.
    because it messes with formatting), this function can be used to get rid of
    it.
    """
    while len(nodes) == 1 and isinstance(nodes[0], _nodes.paragraph):
        nodes = nodes[0].children
    return nodes


def comma_separated_list(parse_me):
    """Parse a restructured text option as a comma-separated list of strings."""
    return parse_me.split(",")
