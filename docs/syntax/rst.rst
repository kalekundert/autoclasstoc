*****************
Restructured Text
*****************

The following directive can be used in any restructured text file:

.. rst:directive:: .. autoclasstoc:: [qualified class name]

  Create a table of contents (TOC) for the given Python class.

  The TOC contains a link to each method defined in the given class.  By 
  default, the links are organized into four groups: "Public Attributes", 
  "Public Methods", "Private Attributes", and "Private Methods".  Public 
  attributes/methods are those with names that either don't begin with an 
  underscore or begin and end with two underscores (i.e.  "dunder methods").  
  Every other attribute/method is private.  It's easy to define custom 
  sections; see :doc:`/advanced_usage` for more details.
  
  In addition to attributes directly defined in the given class, the TOC will 
  also include links to inherited attributes.  These links are grouped by the 
  class they are inherited from, and are collapsed by default to keep the TOC 
  succinct.

  The ``[qualified class name]`` argument is optional if this directive occurs 
  within an :rst:dir:`autoclass` or a :rst:dir:`py:class` directive (in which 
  case the class name can be inferred from the context).  If this argument is 
  provided, it must be the full name of the class, in the same manner expected 
  by :rst:dir:`autoclass`.

  .. rst:directive:option:: sections

      A comma-separated list of sections to include in the class TOC.  If 
      specified, this supercedes the :confval:`autoclasstoc_sections` setting 
      from ``conf.py``.  

  .. rst:directive:option:: exclude-sections

      A comma-separated list of sections to exclude from the class TOC.  This 
      can be used in conjunction with the ``:sections:`` option above.  No 
      sections are excluded by default.

  .. note::

    The "class TOCs" created by this directive are not related to the TOCs 
    defined by :rst:dir:`toctree`.  The term TOC is just used to mean an 
    organized list of links to more detailed documentation.
