************
pathlib.Path
************

The snippet below shows how :rst:dir:`autoclasstoc` can be used to document the 
:class:`pathlib.Path` class from the Python standard library.  This example 
also includes inheritance.  Note that inherited methods are collapsed in the 
TOC by default, but can easily be expanded.

.. example::

  .. autoclass:: pathlib.Path
    :members:
    :private-members:
    :special-members:
    :inherited-members:
    :undoc-members:

    .. autoclasstoc::


