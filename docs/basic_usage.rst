***********
Basic Usage
***********

Follow these steps to start using :rst:dir:`sphinxclasstocr` in your project:

1. Install ``sphinxclasstocr`` from PyPI::

    $ pip install sphinxclasstocr

2. Enable the ``sphinxclasstocr`` and :ext:`autosummary` extensions for your
   Sphinx project.  The latter is required because ``sphinxclasstocr`` uses it to
   create the TOC.  The snippet below also enables :ext:`autodoc` and
   :ext:`viewcode` to demonstrate a typical configuration, but neither of these
   extensions are required:

   .. code-block:: python
      :caption: conf.py

      extensions = [
              ...
              'sphinxclasstocr',
              'sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.viewcode',
              ...
      ]

   You may also want to configure :rst:dir:`autoclass` to include documentation
   for every member of every class by default (see below).  Some projects shy
   away from doing this because including too many "unimportant" methods can
   hide the "important" ones, but this is much less of a concern with
   ``autoclassdoc``.  The TOC will make it easy for users to find the methods
   they're looking for even in classes with lots of documentation (see the
   :doc:`examples/collections` example).

   .. code-block:: python
      :caption: conf.py

      autodoc_default_options = {
          'members': True,
          'special-members': True,
          'private-members': True,
          'inherited-members': True,
          'undoc-members': True,
          'exclude-members': '__weakref__',
      }

3. Use the :rst:dir:`sphinxclasstocr` directive to add a TOC to a class.  Follow
   the link for a full description of the directive, but typical usage is
   pretty straight-forward.  For example, consider the ``Example`` class in the
   following snippet:

   .. literalinclude:: basic_example.py
      :language: python

   We can document this class using :rst:dir:`sphinxclasstocr` as follows:

   .. example::

       .. autoclass:: basic_example.Example
          :members:
          :special-members:
          :private-members:
          :inherited-members:

          .. sphinxclasstocr::
