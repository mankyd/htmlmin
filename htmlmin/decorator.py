from .main import Minifier

def htmlmin(*args, **kwargs):

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
        
