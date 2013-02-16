.. htmlmin documentation master file, created by
   sphinx-quickstart on Thu Feb 14 22:56:34 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

htmlin
===================================
An HTML Minifier with Seatbelts

.. toctree::

   quickstart
   tutorial
   api


htmlin is an HTML minifier that just works. It comes with safe defaults and
an easily configurable set options. It cam turn this::

  <html>
    <head>
      <title>  Hello, Word!  </title>
    </head>
    <body>
      <p> How are <em>you</em> doing?  </p>
    </body>
  </html>

Into this::

  <html><head><title>Hello, World!</title><body><p> How <em>you</em< doing? </p></body></html>

When we say that htmlmin has 'seatbelts', what we mean is that it comes with
features that you can use to safely minify beyond the defaults, but you have to
put them in yourself. For instance, by default, htmlmin will never minimize the
content between ``<pre>``, ``<textarea>``, ``<script>``, and ``<style>`` tags.
You can also  explicitly tell it to not minify additional tags either globally 
name or by adding the custom ``pre`` attribute to a tag in your HTML. htmlmin 
will remove the ``pre`` attributes as it parses your HTML automatically.

It also includes a command-line tool for easy invocation and integration with
existing workflows.

Features
========

* Safely minify HTML with either a function call or from the command line.
* Extend what elements can and cannot be minified.
* Intelligently remove whitespace completely or reduce to single spaces.
* Properly handles unclosed HTML5 tags.
* Optionally remove comments while marking some comments to keep.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
