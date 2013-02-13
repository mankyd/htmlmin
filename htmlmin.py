import cgi
import re
try:
  from html.parser import HTMLParser
except ImportError:
  from HTMLParser import HTMLParser

PRE_TAGS = ('pre', 'textarea')  # styles and scripts are never minified

whitespace_re = re.compile(r'\s+')

# Tag omission rules:
# http://www.w3.org/TR/html51/syntax.html#optional-tags

class HTMLMinParser(HTMLParser):
  def __init__(self, 
               keep_pre=False, 
               pre_tags=PRE_TAGS, 
               keep_comments=True,
               keep_empty=True):
    HTMLParser.__init__(self)
    self.keep_pre = keep_pre
    self.pre_tags = pre_tags
    self.keep_comments = keep_comments
    self.keep_empty = keep_empty
    self._data_buffer = ''
    self._in_pre_tag = 0
    self._body_started = False

    self._tag_stack = []

  def _has_pre(self, attrs):
    for k,v in attrs:
      if k == 'pre':
        return True
    return False

  def build_tag(self, tag, attrs, close_tag):
    result = '<{}'.format(cgi.escape(tag))
    for k,v in attrs:
      result += ' ' + cgi.escape(k)
      if v is not None:
        result += '="{}"'.format(cgi.escape(v))
    if close_tag:
      return result + ' />'
    return result + '>'

  def handle_decl(self, decl):
    self._data_buffer += '<!' + decl + '>\n'

  def in_tag(self, *tags):
    for t in self._tag_stack:
      if t[0] in tags:
        return t
    return False

  def _close_tags_up_to(self, tag):
    num_pres = 0
    for i, t in enumerate(self._tag_stack):
      if t[1]:
        num_pres += 1
      if t[0] == tag:
        break
    self._tag_stack = self._tag_stack[i+1:]

    return num_pres

  def handle_starttag(self, tag, attrs):
    if tag == 'body':
      self._body_started = True

    tag_sets = ( # a list of tags and tags that they are closed by
      (('li',), ('li',)),
      (('dd', 'dt',), ('dd', 'dt',)),
      (('rp', 'rt',), ('rp', 'rt',)),
      (('p',), ('address', 'article', 'aside', 'blockquote', 'dir', 'div', 
                'dl', 'fieldset', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 
                'h5', 'h6', 'header', 'hgroup', 'hr', 'menu', 'nav', 'ol', 'p',
                'pre', 'section', 'table', 'ul')),
      (('optgroup',), ('optgroup',)),
      (('option',), ('option', 'optgroup')),
      #colgroup?
      (('tbody', 'thead',), ('tbody', 'tfoot')),
      (('tfoot',), ('tbody',)),
      (('tr',), ('tr',)),
      (('td', 'th'), ('td', 'th')),
      )
    for open_tags, closed_by_tags in tag_sets:
      in_tag = self.in_tag(*open_tags)
      if in_tag and tag in closed_by_tags:
        self._in_pre_tag -= self._close_tags_up_to(in_tag[0])

    start_pre = False
    if (tag in self.pre_tags or 
        tag in ('script', 'style') or 
        self._has_pre(attrs) or 
        self._in_pre_tag > 0):
      self._in_pre_tag += 1
      start_pre = True

    self._tag_stack.insert(0, (tag, start_pre))

    if not self.keep_pre:
      attrs = [(k,v) for k,v in attrs if k != 'pre']

    self._data_buffer += self.build_tag(tag, attrs, False)

  def handle_endtag(self, tag):
    self._in_pre_tag -= self._close_tags_up_to(tag)
    self._data_buffer += '</{}>'.format(cgi.escape(tag))

  def handle_startendtag(self, tag, attrs):
    if not self.keep_pre:
      attrs = [(k,v) for k,v in attrs if k != 'pre']
    self._data_buffer += self.build_tag(tag, attrs, True)

  def handle_comment(self, data):
    if self.keep_comments or data[0] == '!':
      if data[0] == '!':
        data = data[1:]
      self._data_buffer += '<!--{}-->'.format(data)

  def handle_data(self, data):
    if self._in_pre_tag > 0:
      self._data_buffer += data
    else:
      if not self.keep_empty:
        match = whitespace_re.match(data)
        if match and match.end(0) == len(data):
          return

      new_data = whitespace_re.sub(' ' if self._body_started else '', data)
      if not new_data:
        return

      if self._in_pre_tag == 0:
        # If we're not in a pre block, its possible that we append two spaces
        # together, which we want to avoid. For instance, if we remove a comment
        # from between two blocks of text: a <!-- B --> c => a  c.
        if new_data[0] == ' ' and self._data_buffer[-1] == ' ':
          new_data = new_data[1:]
      self._data_buffer += new_data

  def handle_entityref(self, data):
    self._data_buffer += '&{};'.format(data)

  def handle_charref(self, data):
    self._data_buffer += '&#{};'.format(data)

  def handle_pi(self, data):
    self._data_buffer += '<?' + data + '>'

  def unknown_decl(self, data):
    self._data_buffer += '<![' + data + ']>'

  def reset(self):
    self._data_buffer = ''
    HTMLParser.reset(self)

  @property
  def result(self):
    return self._data_buffer

def minify(input, **kwargs):
  minifier = HTMLMinParser(**kwargs)
  minifier.feed(input)
  minifier.close()
  return minifier.result

class Minifier(object):
  def __init__(self):
    self._parser = HTMLMinParser()

  def input(self, input):
    self._parser.feed(input)

  @property
  def output(self):
    return self._parser.result

  def finalize(self):
    self._parser.close()
    result = self._parser.result
    self._parser.reset()
    return result

  def minify(self, input):
    self._parser.reset()
    self.input(input)
    return self.finalize()
