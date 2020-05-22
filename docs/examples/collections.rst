*******************
collections.Counter
*******************

The snippet below shows how :rst:dir:`autoclasstoc` can be used to document the 
:class:`collections.Counter` class from the Python standard library.  Even 
though this class has a lot of documentation, the TOC makes it easy to (i) 
quickly get a sense for the what the class can do and (ii) quickly navigate to 
the detailed description for any method.

.. example::

  .. autoclass:: collections.Counter
    :members:
    :private-members:
    :special-members:
    :inherited-members:
    :undoc-members:

    .. autoclasstoc::

