=====================
**sphinx-class-tocr**
=====================

|

.. image:: docs/_static/imgs/logo/logo-sphinxclasstocr-1280x640.png
   :alt: sphinxclasstocr

|

|made-with-sphinx-doc|

.. |made-with-sphinx-doc| image:: https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg
   :target: https://www.sphinx-doc.org/


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

sphinxclasstocr is a fork of this excellent project
`autoclasstoc <https://github.com/kalekundert/autoclasstoc/>`__.

*Work is in progress to modify autoclasstoc to meet the needs of our projects.*

**An installation package does not exist yet!**

Check out the :doc:`CHANGELOG <CHANGELOG>` to see what has been done so far to
get ready.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

-----------
What is it?
-----------

A `Sphinx <https://www.sphinx-doc.org/en/master/>`__ plugin to add a TOC like
grouping capability to
`sphinx.ext.autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`__.

--------------
How does it?
--------------


sphinx-class-tocr provides a new Restructured Text directive that gives you the
flexibility to include or exclude class members, depending on the specific
needs of your project.

To help your end-user, you can

#. Include every method of a class.

#. Organise what you want to include into sections.

#. Create *sections* or use the defaults included for a quick setup.

#. Collapse inherited methods to improve readability.

It works well with `sphinx.ext.autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`__
and `sphinx-autogen <https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html>`__.


-----------
Why use it?
-----------

To improve your user's experience, reading your projects automatically
generated API documentation, compared to using
`sphinx.ext.autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`__
alone.


---------------
When to use it?
---------------

sphinx-class-tocr can be incorporated into any new or existing project.



See the `documentation`__ for more information, how to's and examples.

__ https://sphinxclasstocr.readthedocs.io/en/latest/index.html
