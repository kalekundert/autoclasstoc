#!/usr/bin/env python3

import inspect
from docutils import nodes as _nodes
from . import utils

SECTIONS = {}

class Section:
    """
    Format a specific section in a class TOC, e.g. "Public Methods".

    The purpose of this class is to make it easy to customize the sections that 
    make up the class TOC.  For example, you might want an "Event Handler" 
    section that includes any method that starts with "on\_".  Or you might 
    want to format the links in a table with multiple columns, to save more 
    space.  

    These kinds of things can be accomplished by subclassing `Section` and 
    overwriting the relevant methods.  Almost every method is meant to be 
    overridden by subclasses, but most subclasses will only need to override 
    `key`, `title`, and `predicate`.  `key` and `title` have no default value, 
    and must be overridden in each subclass.  `predicate` determines which 
    attributes are included in the section, which is the primary purpose of 
    most custom sections.
    """

    key = None
    """
    A string that can be used to refer to this section, e.g. in ``conf.py`` 
    settings such as :confval:`autoclasstoc_sections` and 
    :rst:dir:`autoclasstoc` options such as ``:sections:`` and 
    ``:exclude-sections:``.
    """
    
    title = None
    """
    The text that will be used to label this section.
    """

    include_inherited = True
    """
    Whether or not to include inherited attributes in this section.
    """

    def __init__(self, state, cls):
        """
        Create a section for a specific class.

        Arguments:
            state (docutils.parsers.rst.states.RSTState): The state object 
                associated with the :rst:dir:`autoclasstoc` directive.  This 
                can be used to evaluate restructured text markup using 
                `nodes_from_rst()`.  cls (type): The class to make the TOC 
                section for.
        """
        self.state = state
        self.cls = cls

    def __init_subclass__(cls):
        """
        Keep track of any `Section` subclasses that are defined.
        """
        SECTIONS[cls.key] = cls

    def check(self):
        """
        Raise `ConfigError` if the section has not been configured correctly, 
        e.g. if it doesn't have a title specified.
        """
        if not self.key:
            raise ConfigError(f"no key specified for {self.__class__.__name__!r}")
        if not self.title:
            raise ConfigError(f"no title specified for {self.__class__.__name__!r}")

    def format(self):
        """
        Return a list of *docutils* nodes that will compose the section.

        The default implementation of this method creates and populates 
        :rst:dir:`autosummary` directives for the class in question and all of 
        its superclasses.  Almost all of 
        """
        assert self.state
        assert self.cls

        wrapper = self._make_container()
        wrapper += self._make_rubric()

        attrs = self._filter_attrs(self.cls.__dict__)
        if not attrs:
            return []

        wrapper += self._make_links(attrs)

        if not self.include_inherited:
            return [wrapper]

        for parent, all_attrs in self._find_inherited_attrs().items():
            attrs = self._filter_attrs(all_attrs)
            if not attrs:
                continue

            d = self._make_inherited_details(parent)
            d += self._make_links(attrs)
            wrapper += d

        return [wrapper]

    def predicate(self, name, attr):
        """
        Return true if the given attribute should be included in this section.

        Arguments:
            name (str): The name of the argument.  In most cases, this is 
                identical to ``attr.__name__``.
            attr (object): The attribute instance itself.

        See Also:
            `is_method`
            `is_attribute`
            `is_public`
            `is_private`
        """
        raise NotImplementedError

    def _make_container(self):
        """
        Create the container node that will contain the entire section.

        This method is meant to be overridden in subclasses.  The primary 
        purpose of the container node is to belong to a CSS class that can then 
        be used to identify HTML elements associated with 
        :rst:dir:`autoclasstoc`.
        """
        return utils.make_container()

    def _make_rubric(self):
        """
        Create the section header node.

        This method is meant to be overridden in subclasses.
        """
        return utils.make_rubric(self.title)

    def _make_links(self, attrs):
        """
        Make a link to the full documentation for each attribute.

        This method is meant to be overridden in subclasses.  The default 
        implementation creates the links using an :rst:dir:`autosummary` 
        directive.

        Arguments:
            attrs (dict): A dictionary of attributes, in the same format as 
                ``__dict__``.
        """
        return utils.make_links(self.state, attrs)

    def _make_inherited_details(self, parent):
        """
        Make a collapsible node to contain links to inherited attributes.

        This method is meant to be overridden in subclasses.  The default 
        implementation returns a `details` node, which is rendered in HTML as a 
        ``<details>`` element.
        """
        return utils.make_inherited_details(self.state, parent)

    def _filter_attrs(self, attrs):
        """
        Return only those attributes that match the predicate.

        Arguments:
            attrs (dict): A dictionary of attributes, in the same format as 
                ``__dict__``.

        Return:
            A dictionary in the same format as *attrs*.
        """
        return utils.filter_attrs(attrs, self.predicate)

    def _find_inherited_attrs(self):
        """
        Find attributes that this class has inherited from other classes.
        """
        return utils.find_inherited_attrs(self.cls)

class PublicMethods(Section):
    """
    Include a "Public Methods" section in the class TOC.
    """
    key = 'public-methods'
    title = "Public Methods:"

    def predicate(self, name, attr):
        return is_method(name, attr) and is_public(name)


class PrivateMethods(Section):
    """
    Include a "Private Methods" section in the class TOC.
    """
    key = 'private-methods'
    title = "Private Methods:"

    def predicate(self, name, attr):
        return is_method(name, attr) and is_private(name)

class PublicAttributes(Section):
    """
    Include a "Public Attributes" section in the class TOC.
    """
    key = 'public-attrs'
    title = "Public Attributes:"

    def predicate(self, name, attr):
        return is_attribute(attr) and is_public(name)

class PrivateAttributes(Section):
    """
    Include a "Private Attributes" section in the class TOC.
    """
    key = 'private-attrs'
    title = "Private Attributes:"

    def predicate(self, name, attr):
        return is_attribute(attr) and is_private(name)

class InnerClasses(Section):
    """
    Include an "Inner Classes" section in the class TOC.
    """
    key = 'inner-classes'
    title = "Inner Classes:"

    def predicate(self, name, attr):
        return inspect.isclass(attr)

def is_method(name, attr):
    """
    Return true if the given attribute is a method or property.
    """
    if name in ['__weakref__', '__dict__']:
        return False

    return any([
        inspect.isfunction(attr),
        inspect.isdatadescriptor(attr),
        inspect.ismethoddescriptor(attr),
    ])

def is_attribute(name, attr):
    """
    Return true if the given attribute is not a method or an inner class.
    """
    return all([
        not inspect.isclass(attr),
        not inspect.isfunction(attr),
        not inspect.isdatadescriptor(attr),
        not inspect.ismethoddescriptor(attr),
    ])

def is_public(name):
    """
    Return true if the given name is public.

    Specifically, a name is public if it either doesn't start with an 
    underscore, or if it starts and ends with two underscores (i.e. a "dunder" 
    method).
    """
    dunder = name.startswith('__') and name.endswith('__')
    return dunder or not name.startswith('_')

def is_private(name):
    """
    Return true if the given name is private.
    """
    return not is_public(name)

