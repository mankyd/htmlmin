.. htmlmin documentation master file, created by
   sphinx-quickstart on Thu Feb 14 22:56:34 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

htmlmin
===================================
An HTML Minifier with Seatbelts

.. toctree::

   quickstart
   tutorial
   reference


htmlmin is an HTML minifier that just works. It comes with safe defaults and
an easily configurable set options. It can turn this::

  <html>
    <head>
      <title>  Hello, World!  </title>
    </head>
    <body>
      <p> How are <em>you</em> doing?  </p>
    </body>
  </html>

Into this::

  <html><head><title>Hello, World!</title><body><p> How are <em>you</em> doing? </p></body></html>

When we say that htmlmin has 'seatbelts', what we mean is that it comes with
features that you can use to safely minify beyond the defaults, but you have to
put them in yourself. For instance, by default, htmlmin will never minimize the
content between ``<pre>``, ``<textarea>``, ``<script>``, and ``<style>`` tags.
You can also  explicitly tell it to not minify additional tags either globally
by name or by adding the custom ``pre`` attribute to a tag in your HTML. htmlmin
will remove the ``pre`` attributes as it parses your HTML automatically.

It also includes a command-line tool for easy invocation and integration with
existing workflows.

Install
=======

To install via pip::

  pip install htmlmin

Source Code
===========

Source code is availble on github at
`https://github.com/mankyd/htmlmin <https://github.com/mankyd/htmlmin>`_::

  git clone git://github.com/mankyd/htmlmin.git

Features
========

* Safely minify HTML with either a :class:`function call <htmlmin.minify>` or
  from the :ref:`command line <command_line>`.
* Extend what elements can and cannot be minified.
* Intelligently remove whitespace completely or reduce to single spaces.
* Properly handles unclosed HTML5 tags.
* Optionally remove comments while marking some comments to keep.
* Simple function :class:`decorator <htmlmin.decorator.htmlmin>` to minify all
  function output.
* Simple :class:`WSGI middleware <htmlmin.middleware.HTMLMinMiddleware>` to
  minify web app output.
* `Tested <https://travis-ci.org/mankyd/htmlmin>`_ in both Python 2.7 and 3.2:
  |build_status|

.. |build_status| image:: https://travis-ci.org/mankyd/htmlmin.png?branch=master

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
