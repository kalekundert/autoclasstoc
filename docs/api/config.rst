*************
Configuration
*************
The following setting can be defined in ``conf.py``:

.. confval:: autoclasstoc_sections

  The default list of sections to include in class TOCs.  The values in the 
  list can be either strings or `Section` classes.  Strings are the same values 
  that can be provided to the section options of the :rst:dir:`autoclasstoc` 
  directive, and must refer to the name of a section class.  The following 
  section names are available by default:

  - ``public-methods``: Methods and properties that don't begin with an 
    underscore (or that are special methods, e.g. :py:meth:`__init__`).
  - ``private-methods``: Methods and properties that begin with an underscore.
  - ``public-attrs``: Non-methods and non-classes that don't begin with an 
    underscore.
  - ``private-attrs``: Non-methods and non-classes that begin with an 
    underscore.
  - ``inner-classes``: Classes defined within the class in question.

  The names of any custom `Section` classes that have been defined can be used 
  as well.  The default value for this setting is::

    autoclasstoc_sections = ['public-methods', 'private-methods']
