.. Findmyreviewers documentation master file, created by
   sphinx-quickstart on Sat May 27 16:04:53 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

   author: Alan Chen

Welcome to Findmyreviewers's documentation!
===========================================

Findmyreviewers (FMR in short) is an open-source project that extracts *topics* from a piece of text using trained LDA models and tries to find best matching scholars from a pool of scholars.

To create a pool of scholars, we profile each author with their papers using the LDA model, yielding a vector of their fields. This pool of vectors corresponds to the specific LDA model, from which the vectors are generated.

Please refer to following documents for more details:

.. toctree::
   :maxdepth: 2

   installation
   configuration
   database
   customization
   impl
   misc



.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
