from docutils import nodes as _nodes
from docutils.statemachine import StringList, string2lines
from importlib import import_module
from functools import partial
from inspect import isclass
from .errors import ConfigError


def pick_class(qual_name, env):
    """
    Figure out which class to make the TOC for.

    We can either be given this information as an argument, or we can try to 
    figure it out from the context (e.g. the :rst:dir:`autoclass` or 
    :rst:dir:`py:class` currently being processed).

    Arguments:
        qual_name (str): The name of the class to pick, or None if the class 
            should be inferred from the environment.
        env (sphinx.environment.BuildEnvironment): This object is available as 
            :attr:`self.env` from :class:`~sphinx.util.docutils.SphinxDirective` 
            subclasses.
    """
    if qual_name:
        mod_name, cls_name = qual_name.rsplit('.', 1)
        xref_factory = get_cls_xref
    else:
        cls_name = \
            env.temp_data.get('autodoc:class') or \
            env.ref_context.get('py:class')
        mod_name = \
            env.temp_data.get('autodoc:module') or \
            env.ref_context.get('py:module')
        xref_factory = partial(get_cls_xref, implied_mod=f'{mod_name}.')

        if not cls_name:
            raise ConfigError("no class name")
        if not mod_name:
            raise ConfigError("no module name")

    return mod_name, cls_name, xref_factory


def load_class(mod_name, cls_name):
    """
    Import the given class from the given module.
    """
    mod = import_module(mod_name)
    cls = getattr(mod, cls_name)
    return mod, cls


def pick_sections(sections, exclude=None):
    """
    Determine which sections to include in the class TOC.

    The return value will be a list in the same order as *sections*, but with 
    any sections from *exclude* removed.  Both arguments can specify sections 
    using string names (e.g. "public-methods") or un-instantiated `Section` 
    classes.  All names will be converted to classes in the return value.
    """

    def _section_from_anything(x):
        from .sections import Section, SECTIONS

        if isinstance(x, str):
            try:
                return SECTIONS[x]
            except KeyError:
                raise ConfigError(f"no autoclasstoc section with key {x!r}")

        if isclass(x) and issubclass(x, Section):
            return x

        raise ConfigError(f"cannot interpret {x!r} as a section")

    sections = [
        _section_from_anything(x)
        for x in sections
    ]
    exclude = {
        _section_from_anything(x)
        for x in exclude or []
    }
    return [
        x
        for x in sections
        if x not in exclude
    ]


def make_toc(state, cls, xref_factory, sections):
    """
    Create the class TOC.
    """
    n = []
    for section_cls in sections:
        section = section_cls(state, cls, xref_factory)
        section.check()
        n += section.format()

    n.append(_nodes.transition())
    return n


def make_container():
    """
    Make a container node to identify elements associated with the 
    :rst:dir:`autoclasstoc` directive.
    """
    return _nodes.container(classes=['autoclasstoc'])


def make_rubric(title):
    """
    Make an informal header.
    """
    return _nodes.rubric(title, title)


def make_inherited_details(state, parent, open_by_default=False):
    """
    Make a collapsible node to contain information about inherited attributes.
    """
    from .nodes import details, details_summary

    s = details_summary()
    s += strip_p(nodes_from_rst(state, f"Inherited from :py:class:`{get_cls_xref(parent)}`"))

    d = details(open_by_default)
    d += s
    return d

def make_links(state, attrs, cls, xref_factory):
    """
    Make links to the given class attributes.

    More specifically, the links are made using the :rst:dir:`autosummary` 
    directive.
    """
    assert attrs

    cls_xref = xref_factory(cls, if_cant_import='')

    return nodes_from_rst(state, [
        '.. autosummary::',
        '',
        *[f'    {join(cls_xref, x, sep=".")}' for x in attrs],
    ])


def get_cls_xref(cls, *, if_cant_import=None, implied_mod=None):
    """
    Return a RST-formatted string that references the given class.

    The purpose of this function is to handle the special case where the class 
    in question can't be imported.  Currently, this case is checked for using a 
    simple heuristic: whether the class's qualified name includes any local 
    namespaces.  If this is the case, the return value can be chosen to avoid 
    triggering any Sphinx/autodoc errors and to produce output that is at least 
    reasonable.
    """

    if '<locals>' in cls.__qualname__:
        return cls.__name__ if if_cant_import is None else if_cant_import
    else:
        xref = f'{cls.__module__}.{cls.__qualname__}'
        if implied_mod and xref.startswith(implied_mod):
            xref = xref[len(implied_mod):]
        return f'~{xref}'


def find_attrs(cls):
    """
    Return a dictionary containing every attribute of the given class.

    This dictionary is very similar to ``__dict__``, except that it also 
    includes attributes that have annotations but not values.  Such attributes 
    are assigned the sentinel value `ANNOTATED_ATTR`.
    """
    annotated_attrs = {
            k: ANNOTATED_ATTR

            # This is the recommended way to get the annotations for a class 
            # object, prior to the introduction of `inspect.get_annotations()` 
            # in python 3.10 [1].  The awkward `__dict__.get()` syntax is to 
            # avoid getting the parent class annotations if the child class 
            # doesn't have any.
            #
            # [1]: https://docs.python.org/3/howto/annotations.html#accessing-the-annotations-dict-of-an-object-in-python-3-9-and-older
            for k in cls.__dict__.get('__annotations__', {})

            if k not in cls.__dict__
    }
    return {**cls.__dict__, **annotated_attrs}


def find_inherited_attrs(cls):
    """
    Return a dictionary mapping parent classes to the attributes inherited from 
    those classes.
    """
    return {
        base: find_attrs(base)
        for base in cls.__mro__
        if base not in (cls, object)
    }


def filter_attrs(attrs, predicate):
    """
    Remove attributes for which the given predicate function returns False.
    """
    from inspect import getdoc

    try:
        # sphinx>=4
        from sphinx.util.docstrings import separate_metadata
        get_meta = lambda doc: separate_metadata(doc)[1]
    except ImportError:
        # sphinx<4
        from sphinx.util.docstrings import extract_metadata
        get_meta = extract_metadata

    return {
        k: v
        for k, v in attrs.items()
        if predicate(k, v, get_meta(getdoc(v)))
    }


def nodes_from_rst(state, rst):
    """
    Create nodes from the given restructured text.

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
    """
    Remove any top-level paragraph nodes.

    Parsing a simple string like "Hello world" with `nodes_from_rst` will 
    return text wrapped in a paragraph.  If this paragraph is not desired (e.g.  
    because it messes with formatting), this function can be used to get rid of 
    it.
    """
    while len(nodes) == 1 and isinstance(nodes[0], _nodes.paragraph):
        nodes = nodes[0].children
    return nodes


def comma_separated_list(x):
    """
    Parse a restructured text option as a comma-separated list of strings.
    """
    return x.split(',')


def join(*strs, sep=''):
    """
    Concatenate the given strings, excluding any that are empty.
    """
    return sep.join(x for x in strs if x)

ANNOTATED_ATTR = object()
"""
A special value used to represent attributes that are annotated, but assigned 
no value.

This value can appear in the dictionary passed to `filter_attrs()`.
"""
