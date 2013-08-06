Quickstart
==========
For single invocations, there is the :class:`htmlmin.minify`
method. It takes input html as a string for its first argument and returns
minified html. It accepts multiple different options that allow you to tune the
amount of minification being done, with the defaults being the safest available
options::

  >>> import htmlmin
  >>> input_html = '''
    <body   style="background-color: tomato;">
      <h1>  htmlmin   rocks</h1>
      <pre>
        and rolls
      </pre>
    </body>'''
  >>> htmlmin.minify(input_html)
  u' <body style="background-color: tomato;"> <h1> htmlmin rocks</h1> <pre>\n        and rolls\n      </pre> </body>'
  >>> print htmlmin.minify(input_html)
   <body style="background-color: tomato;"> <h1> htmlmin rocks</h1> <pre>
          and rolls
        </pre> </body>

If there is a chunk of html which you do not want minified, put a ``pre``
attribute on an HTML tag that wraps it. htmlmin will leave the contents of the
tag alone and will remove the ``pre`` attribute before it is output::

  >>> import htmlmin
  >>> input_html = '''<span>   minified   </span><span pre>   not minified   </span>'''
  >>> htmlmin.minify(input_html)
  u'<span> minified </span><span>   not minified   </span>'

The :class:`minify <htmlmin.minify>` function works well for one off
minifications. However, if you are going to minify several pieces of HTML, the
:class:`Minifier <htmlmin.Minifier>` class is provided. It works similarly, but
allows for persistence of options between invocations and recycles the internal
data structures used for minification.

.. _command_line:

Command Line
------------
htmlmin is invoked by running::

  htmlmin input.html output.html

If no output file is specified, it will print to ``stdout``. If no input
specified, it reads form ``stdin``. Help with options can be retrieved at
any time by running `htmlmin -h`::

  htmlmin -h
  usage: htmlmin [-h] [-c] [-s] [--remove-all-empty-space] [-H] [-k] [-p [TAG [TAG ...]]] [-e ENCODING]
                 [INPUT] [OUTPUT]

  Minify HTML

  positional arguments:
    INPUT                 File path to html file to minify. Defaults to stdin.
    OUTPUT                File path to output to. Defaults to stdout.

  optional arguments:
    -h, --help            show this help message and exit
    -c, --remove-comments
                          When set, comments will be removed. They can be kept on an individual basis
                          by starting them with a '!': <!--! comment -->. The '!' will be removed from
                          the final output. If you want a '!' as the leading character of your comment,
                          put two of them: <!--!! comment -->.

    -s, --remove-empty-space
                          When set, this removes empty space betwen tags in certain cases. 
                          Specifically, it will remove empty space if and only if there a newline
                          character occurs within the space. Thus, code like 
                          '<span>x</span> <span>y</span>' will be left alone, but code such as
                          '   ...
                            </head>
                            <body>
                              ...'
                          will become '...</head><body>...'. Note that this CAN break your 
                          html if you spread two inline tags over two lines. Use with caution.

    --remove-all-empty-space
                          When set, this removes ALL empty space betwen tags. WARNING: this can and
                          likely will cause unintended consequences. For instance, '<i>X</i> <i>Y</i>'
                          will become '<i>X</i><i>Y</i>'. Putting whitespace along with other text will
                          avoid this problem. Only use if you are confident in the result. Whitespace is
                          not removed from inside of tags, thus '<span> </span>' will be left alone.

    -H, --in-head         If you are parsing only a fragment of HTML, and the fragment occurs in the
                          head of the document, setting this will remove some extra whitespace.

    -k, --keep-pre-attr   HTMLMin supports the propietary attribute 'pre' that can be added to elements
                          to prevent minification. This attribute is removed by default. Set this flag to
                          keep the 'pre' attributes in place.

    -a PRE_ATTR, --pre-attr PRE_ATTR
                          The attribute htmlmin looks for to find blocks of HTML that it should not 
                          minify. This attribute will be removed from the HTML unless '-k' is
                          specified. Defaults to 'pre'.

    -p [TAG [TAG ...]], --pre-tags [TAG [TAG ...]]
                          By default, the contents of 'pre', and 'textarea' tags are left unminified.
                          You can specify different tags using the --pre-tags option. 'script' and 'style'
                          tags are always left unmininfied.

    -e ENCODING, --encoding ENCODING
                          Encoding to read and write with. Default 'utf-8'.
