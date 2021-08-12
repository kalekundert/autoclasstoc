***************
sphinxclasstocr
***************

.. image:: https://readthedocs.org/projects/sphinxclasstocr/badge/?version=latest
   :target: https://sphinxclasstocr.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code style: black

|

**sphinxclasstocr is a fork of this excellent project
`autoclasstoc <https://github.com/kalekundert/autoclasstoc/>`__.**

*Work is in progress to modify autoclasstoc to meet the needs of our projects.*

Check out the CHANGELOG to see what has been done so far to get ready.

**See the unmodified excellent description of autoclasstoc by the author below.**


It's surprisingly difficult to document large Python classes in a way that's
easy for users to navigate.  Most projects use the ``autodoc`` Sphinx plugin,
which simply puts the complete documentation for each class member one after
another.  While this does fully document the class, it doesn't give the user a
quick way to see everything the class can do.  This makes classes of even
moderate complexity difficult to navigate.  It also encourages projects to be
stingy about which class members to include in the documentation (e.g.
excluding special methods, inherited methods, private methods, and/or
undocumented methods), to the further detriment of the user.

What's needed is for each class to have a succinct table of contents (TOC)
that:

- Is organized into sections that will be meaningful to the user.  Different
  projects and classes may call for different sections, e.g. public/private
  methods, methods that share a decorator, methods with a common prefix, etc.

- Includes every method of the class (so that the documentation is complete),
  while still making it easy for the user to get a sense for what the class
  does and find what they're looking for.

- Collapses inherited methods.  Complex classes in particular can inherit a lot
  of methods from their parent classes, and while these methods should be
  present in the TOC (since they're part of the class), collapsing them makes
  it easier for the user to grok the functionality provided by the class
  itself.

``sphinxclasstocr`` provides a new Restructured Text directive that is all of
these things.  It also works well with ``autodoc`` and ``autogen``, and should
be easy to incorporate into any existing project.

See the `complete documentation`__ for more information (including examples).

__ https://sphinxclasstocr.readthedocs.io/en/latest/index.html
