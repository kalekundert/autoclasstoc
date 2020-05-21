********************
Sphinx Configuration
********************
The following setting can be defined in ``conf.py``:

.. confval:: autoclasstoc_sections

  The default list of sections to include in class TOCs, in the order they 
  should appear in the documentation.  The values in the list can be either 
  strings or `Section` classes.  Strings are the same values that can be 
  provided to the section options of the :rst:dir:`autoclasstoc` directive, and 
  must refer to the name of a section class.  The following section names are 
  available by default:

  ``public-methods``
    Methods that don't begin with an underscore (or that are special methods, 
    e.g. :py:meth:`__init__`).

  ``private-methods``
    Methods that do begin with an underscore (and are not special).

  ``public-attrs``
    Non-methods and non-classes that don't begin with an underscore.

  ``private-attrs``
    Non-methods and non-classes that begin with an underscore.

  ``inner-classes``
    Classes defined within the class in question.

  The names of any :ref:`custom sections <Custom sections>` that have been 
  defined can be used as well.  The default value for this setting is::

    autoclasstoc_sections = [
            'public-attrs',
            'public-methods',
            'private-attrs',
            'private-methods',
    ]
