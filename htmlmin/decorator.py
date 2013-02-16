from .main import Minifier

def htmlmin(*args, **kwargs):
  """Minifies HTML that is returned by a function.

  A simple decorator that minifies the HTML output of any function that it
  decorates. It supports all the same options that :class:`htmlmin.minify` has.
  With no options, it uses ``minify``'s default settings::

      @htmlmin
      def foobar():
         return '   minify me!   '

  or::

      @htmlmin(remove_comments=True)
      def foobar():
         return '   minify me!  <!-- and remove me! -->'
  """
  def _decorator(fn):
    minify = Minifier(**kwargs).minify
    def wrapper(*a, **kw):
      return minify(fn(*a, **kw))
    return wrapper

  if len(args) == 1:
    if callable(args[0]) and not kwargs:
      return _decorator(args[0])
    else:
      raise RuntimeError(
          'htmlmin decorator does accept positional arguments')
  elif len(args) > 1:
    raise RuntimeError(
      'htmlmin decorator does accept positional arguments')
  else:
    return _decorator
        
