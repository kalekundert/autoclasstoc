******
Python
******
.. module:: autoclasstoc

The primary purpose of the Python API is to define :ref:`custom sections 
<Custom sections>` for the class TOCs.  This is done by subclassing the 
`Section` class, although a number of helper functions and classes are also 
available.

.. autosummary::
  :toctree: api
  :recursive:

  autoclasstoc.AutoClassToc
  autoclasstoc.Section
  autoclasstoc.PublicMethods
  autoclasstoc.PrivateMethods
  autoclasstoc.PublicDataAttrs
  autoclasstoc.PrivateDataAttrs
  autoclasstoc.InnerClasses
  autoclasstoc.is_method
  autoclasstoc.is_data_attr
  autoclasstoc.is_public
  autoclasstoc.is_private
  autoclasstoc.is_special
  autoclasstoc.utils
  autoclasstoc.nodes
  autoclasstoc.ConfigError
