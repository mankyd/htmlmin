import cgi
import re

from . import parser

def minify(input,
           remove_comments=False,
           remove_empty_space=False,
           remove_all_empty_space=False,
           keep_pre=False,
           pre_tags=parser.PRE_TAGS,
           pre_attr='pre'):
  """Minifies HTML in one shot.

  :param input: A string containing the HTML to be minified.
  :param remove_comments: Remove comments found in HTML. Individual comments can
    be maintained by putting a ``!`` as the first character inside the comment.
    Thus::

       <!-- FOO --> <!--! BAR -->

    Will become simply::

       <!-- BAR -->

    The added exclamation is removed.
  :param remove_empty_space: Remove empty space found in HTML between an opening
    and a closing tag and when it contains a newline or carriage return. If
    whitespace is found that is only spaces and/or tabs, it will be turned into
    a single space. Be careful, this can have unintended consequences.
  :param remove_all_empty_space: A more extreme version of
    ``remove_empty_space``, this removes all empty whitespace found between
    tags. This is almost gauranteed to break your HTML unless you are very
    careful.
    nothing
  :param keep_pre: By default, htmlmin uses the special attribute ``pre`` to
    allow you to demarcate areas of HTML that should not be minified. It removes
    this attribute as it finds it. Setting this value to ``True`` tells htmlmin
    to leave the attribute in the output.
  :param pre_tags: A list of tag names that should never be minified. You are
    free to change this list as you see fit, but you will probably want to
    include ``pre`` and ``textarea`` if you make any changes to the list. Note
    that ``<script>`` and ``<style>`` tags are never minimized.
  :param pre_attr: Specifies the attribute that, when found in an HTML tag, 
    indicates that the content of the tag should not be minified. Defaults to
    ``pre``.
  :return: A string containing the minified HTML.

  If you are going to be minifying multiple HTML documents, each with the same
  settings, consider using :class:`.Minifier`.
  """
  minifier = parser.HTMLMinParser(
      remove_comments=remove_comments,
      remove_empty_space=remove_empty_space,
      remove_all_empty_space=remove_all_empty_space,
      keep_pre=keep_pre,
      pre_tags=pre_tags,
      pre_attr=pre_attr)
  minifier.feed(input)
  minifier.close()
  return minifier.result

class Minifier(object):
  """An object that supports HTML Minification.

  Options are passed into this class at initialization time and are then 
  persisted across each use of the instance. If you are going to be minifying
  multiple peices of HTML, this will be more efficient than using
  :class:`htmlmin.minify`.

  See :class:`htmlmin.minify` for an explanation of options.
  """

  def __init__(self,
               remove_comments=False,
               remove_empty_space=False,
               remove_all_empty_space=False,
               keep_pre=False,
               pre_tags=parser.PRE_TAGS,
               pre_attr='pre'):
    """Initialize the Minifier.

    See :class:`htmlmin.minify` for an explanation of options.
    """
    self._parser = parser.HTMLMinParser(
      remove_comments=remove_comments,
      remove_empty_space=remove_empty_space,
      remove_all_empty_space=remove_all_empty_space,
      keep_pre=keep_pre,
      pre_tags=pre_tags,
      pre_attr=pre_attr)

  def minify(self, *input):
    """Runs HTML through the minifier in one pass.

    :param input: HTML to be fed into the minimizer. Multiple chunks of HTML
      can be provided, and they are fed in sequentially as if they were
      concatenated.
    :returns: A string containing the minified HTML.

    This is the simplest way to use an existing ``Minifier`` instance. This
    method takes in HTML and minfies it, returning the result. Note that this
    method resets the internal state of  the parser before it does any work. If
    there is pending HTML in the buffers, it will be lost.
    """
    self._parser.reset()
    self.input(*input)
    return self.finalize()

  def input(self, *input):
    """Feed more HTML into the input stream

    :param input: HTML to be fed into the minimizer. Multiple chunks of HTML
      can be provided, and they are fed in sequentially as if they were
      concatenated. You can also call this method multiple times to achieve
      the same effect.
    """
    for i in input:
      self._parser.feed(i)

  @property
  def output(self):
    """Retrieve the minified output generated thus far.
    """
    return self._parser.result

  def finalize(self):
    """Finishes current input HTML and returns mininified result.

    This method flushes any remaining input HTML and returns the minified 
    result. It resets the state of the internal parser in the process so that
    new HTML can be minified. Be sure to call this method before you reuse
    the ``Minifier`` instance on a new HTML document.
    """
    self._parser.close()
    result = self._parser.result
    self._parser.reset()
    return result

