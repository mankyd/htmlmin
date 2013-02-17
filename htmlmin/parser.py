import cgi
import re
try:
  from html.parser import HTMLParser
except ImportError:
  from HTMLParser import HTMLParser

PRE_TAGS = ('pre', 'textarea')  # styles and scripts are never minified
NO_CLOSE_TAGS = ('area', 'base', 'br', 'hr', 'img', 'input', 'keygen', 'meta',
                 'param', 'source', 'track', 'wbr')

leading_trailing_whitespace_re = re.compile(r'(^\s+)|(\s+$)')
whitespace_re = re.compile(r'\s+')
whitespace_newline_re = re.compile(r'\s*(\r|\n)+\s*')

# Tag omission rules:
# http://www.w3.org/TR/html51/syntax.html#optional-tags

class HTMLMinError(Exception): pass
class ParseError(HTMLMinError): pass
class OpenTagNotFoundError(ParseError): pass

class HTMLMinParser(HTMLParser):
  def __init__(self,
               remove_comments=False,
               remove_empty_space=False,
               remove_all_empty_space=False,
               keep_pre=False,
               pre_tags=PRE_TAGS,
               pre_attr='pre'):
    HTMLParser.__init__(self)
    self.keep_pre = keep_pre
    self.pre_tags = pre_tags
    self.remove_comments = remove_comments
    self.remove_empty_space = remove_empty_space
    self.remove_all_empty_space = remove_all_empty_space
    self.pre_attr = pre_attr
    self._data_buffer = []
    self._in_pre_tag = 0
    self._in_head = False
    self._after_doctype = False
    self._tag_stack = []

  def _has_pre(self, attrs):
    for k,v in attrs:
      if k == self.pre_attr:
        return True
    return False

  def build_tag(self, tag, attrs, close_tag):
    result = u'<{}'.format(cgi.escape(tag))
    for k,v in attrs:
      result += ' ' + cgi.escape(k)
      if v is not None:
        result += u'="{}"'.format(cgi.escape(v))
    if close_tag:
      return result + '/>'
    return result + '>'

  def handle_decl(self, decl):
    if (len(self._data_buffer) == 1 and 
        whitespace_re.match(self._data_buffer[0])):
      self._data_buffer = []
    self._data_buffer.append('<!' + decl + '>\n')
    self._after_doctype = True

  def in_tag(self, *tags):
    for t in self._tag_stack:
      if t[0] in tags:
        return t
    return False

  def _close_tags_up_to(self, tag):
    num_pres = 0
    i = 0
    for i, t in enumerate(self._tag_stack):
      if t[1]:
        num_pres += 1
      if t[0] == tag:
        break

      # Only the html tag can close out everything. Put on the brakes if
      # we encounter a closing tag that we didn't recognize.
      if tag != 'html' and t[0] in ('body', 'html', 'head'):
        raise OpenTagNotFoundError()

    self._tag_stack = self._tag_stack[i+1:]

    return num_pres

  def handle_starttag(self, tag, attrs):
    self._after_doctype = False
    if tag == 'head':
      self._in_head = True

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
      (('colgroup',), ('*',)),
      (('tbody', 'thead',), ('tbody', 'tfoot')),
      (('tfoot',), ('tbody',)),
      (('tr',), ('tr',)),
      (('td', 'th'), ('td', 'th')),
      )
    for open_tags, closed_by_tags in tag_sets:
      in_tag = self.in_tag(*open_tags)
      if in_tag and (tag in closed_by_tags or '*' in closed_by_tags):
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
      attrs = [(k,v) for k,v in attrs if k != self.pre_attr]

    self._data_buffer.append(self.build_tag(tag, attrs, False))

  def handle_endtag(self, tag):
    # According to the spec, <p> tags don't get closed when a parent a
    # tag closes them. Here's some logic that addresses this.
    if tag == 'a':
      contains_p = False
      for i, t in enumerate(self._tag_stack):
        if t[0] == 'p':
          contains_p = True
        elif t[0] == 'a':
          break
      if contains_p: # the p tag, and all its children should be left open
        a_tag = self._tag_stack.pop(i)
        if a_tag[1]:
          self._in_pre_tag -= 1
    else:
      if tag == 'head':
        # TODO: Did we know that we were in an head tag?! If not, we need to
        # reminify everything to remove extra spaces.
        self._in_head = False
      try:
        self._in_pre_tag -= self._close_tags_up_to(tag)
      except OpenTagNotFoundError:
        # Some tags don't require a start tag. Most do. Either way, we leave
        # closing tags along since they affect output. For instance, a '</p>'
        # results in a '<p></p>' in Chrome.
        pass
    self._data_buffer.append('</{}>'.format(cgi.escape(tag)))

  def handle_startendtag(self, tag, attrs):
    self._after_doctype = False
    if not self.keep_pre:
      attrs = [(k,v) for k,v in attrs if k != 'pre']
    self._data_buffer.append(self.build_tag(tag, attrs, tag not in NO_CLOSE_TAGS))

  def handle_comment(self, data):
    if not self.remove_comments or data[0] == '!':
      self._data_buffer.append('<!--{}-->'.format(
          data[1:] if data[0] == '!' else data))

  def handle_data(self, data):
    if self._in_pre_tag > 0:
      self._data_buffer.append(data)
    else:
      # remove_all_empty_space matches everything. remove_empty_space only 
      # matches if there's a newline involved.
      if self.remove_all_empty_space or self._in_head or self._after_doctype:
        match = whitespace_re.match(data)
        if match and match.end(0) == len(data):
          return
      elif self.remove_empty_space:
        match = whitespace_newline_re.match(data)
        if match and match.end(0) == len(data):
          return
        

      # if we're in the title, remove leading and trailing whitespace
      if self._tag_stack and self._tag_stack[0][0] == 'title':
        data = leading_trailing_whitespace_re.sub('', data)
      data = whitespace_re.sub(' ', data)
      if not data:
        return

      if self._in_pre_tag == 0 and self._data_buffer:
        # If we're not in a pre block, its possible that we append two spaces
        # together, which we want to avoid. For instance, if we remove a comment
        # from between two blocks of text: a <!-- B --> c => a  c.
        if data[0] == ' ' and self._data_buffer[-1][-1] == ' ':
          data = data[1:]
          if not data:
            return
      self._data_buffer.append(data)

  def handle_entityref(self, data):
    self._data_buffer.append('&{};'.format(data))

  def handle_charref(self, data):
    self._data_buffer.append('&#{};'.format(data))

  def handle_pi(self, data):
    self._data_buffer.append('<?' + data + '>')

  def unknown_decl(self, data):
    self._data_buffer.append('<![' + data + ']>')

  def reset(self):
    self._data_buffer = []
    HTMLParser.reset(self)

  @property
  def result(self):
    return ''.join(self._data_buffer)
