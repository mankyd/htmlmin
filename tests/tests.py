import unittest

import htmlmin

MINIFY_FUNCTION_TEXTS = {
  'simple_text': (
    '  a  b',
    ' a b'
  ),
  'long_text': (
    '''When doing     test-driven development, or
    running automated builds that need testing before they are  deployed
\t\t for downloading or use, it's often useful to be able to run a project's
unit tests without actually deploying the project anywhere.\r\n\r\n\n\r\rThe
test command runs project's unit tests without actually deploying it, by
    temporarily putting the project's source on sys.path, after first running
     build_ext -i to ensure that any C extensions are built.

    ''',
    ("When doing test-driven development, or running automated "
      "builds that need testing before they are deployed for "
      "downloading or use, it's often useful to be able to run a "
      "project's unit tests without actually deploying the project "
      "anywhere. The test command runs project's unit tests without "
      "actually deploying it, by temporarily putting the project's "
      "source on sys.path, after first running build_ext -i to "
      "ensure that any C extensions are built. ")
  ),
  'simple_html': (
    (' <body> <b>  a <i pre>b  </i>'  # <b> is not closed
     '<pre>   x </pre> <textarea>   Y  </textarea></body> '),
    (' <body> <b> a <i>b  </i>'
     '<pre>   x </pre> <textarea>   Y  </textarea></body> ')
  ),
}

FEATURES_TEXTS = {
  'remove_tag_name_whitespace': (
    '<body  >  <br   />  <textarea  >   </ textarea  ></  body>  ',
    '<body> <br> <textarea>   </textarea></body> '
  ),
  'remove_comments': (
    '<body> this text should <!-- X --> have comments removed</body>',
    '<body> this text should have comments removed</body>',
  ),
  'keep_comments': (
    '<body> this text should <!--! not --> have comments removed</body>',
    '<body> this text should <!-- not --> have comments removed</body>',
  ),
  'keep_pre': (
    '<body>the <strong pre   style="">pre</strong> should stay  </body>',
    '<body>the <strong pre style="">pre</strong> should stay </body>',
  ),
  'keep_empty': (
    '<body> <div id="x"  >  A </div>  <div id="  y ">  B    </div>  </body>',
    '<body> <div id="x"> A </div> <div id="  y "> B </div> </body>',
  ),
  'remove_empty': (
    '<body> <div id="x"  >  A </div>  <div id="  y ">  B    </div>  </body>',
    '<body><div id="x"> A </div><div id="  y "> B </div></body>',
  ),
  'dont_minify_div': (
    '<body>  <div>   X  </div>   </body>',
    '<body> <div>   X  </div> </body>',
  ),
  'minify_pre': (
    '<body>  <pre>   X  </pre>   </body>',
    '<body> <pre> X </pre> </body>',
  ),
  'remove_head_spaces': (
    '<head>  <title> X  Y </title>  </head>',
    '<head><title>X Y</title></head>',
  ),
  'dont_minify_scripts_or_styles': (
    '<body>  <script>   X  </script>  <style>   X</style>   </body>',
    '<body> <script>   X  </script> <style>   X</style> </body>',
  ),
  'remove_close_from_tags': (
    ('<body> <area/> <base/> <br /> <hr/> <img />   <input   /> <keygen/> '
     '<meta  /><param/><source/><track  /><wbr />  </body>'),
    ('<body> <area> <base> <br> <hr> <img> <input> <keygen> '
     '<meta><param><source><track><wbr> </body>'),
  ),
  'remove_space_from_self_closed_tags': (
    '<body>    <y />   <x    /></body>',
    '<body> <y/> <x/></body>',
  ),
  'in_head': (
    '<link /><script>   </script><title pre>   X </title>    <link />',
    '<link/><script>   </script><title>   X </title><link/>',
  ),
}

SELF_CLOSE_TEXTS = {
  'p_self_close': (
    '<body>  <p pre  >  X  <p>  Y  ',
    '<body> <p>  X  <p> Y ',
  ),
  'li_self_close': (
    '<body> <ul>  <li pre  >  X  <li>  Y  <li pre>  Z</ul>   Q',
    '<body> <ul> <li>  X  <li> Y <li>  Z</ul> Q',
  ),
  'dt_self_close': (
    '<body> <dl>  <dt pre  >  X  <dt>  Y  <dt pre>  Z</dt></dl>   Q',
    '<body> <dl> <dt>  X  <dt> Y <dt>  Z</dt></dl> Q',
  ),
  'dd_self_close': (
    '<body> <dl>  <dd pre  >  X  <dd>  Y  <dd pre>  Z</dl>   Q',
    '<body> <dl> <dd>  X  <dd> Y <dd>  Z</dl> Q',
  ),
  'optgroup_self_close': (
    ('<body>   <select  a >  <optgroup pre>   <option>   X</option>   '
     '<optgroup>   <option>   Y</option> </optgroup> </select>   </body>'),
    ('<body> <select a> <optgroup>   <option>   X</option>   '
     '<optgroup> <option> Y</option> </optgroup> </select> </body>'),
  ),
  'option_self_close': (
    ('<body>   <select  a >  <option pre  >   X    '
     '<option> Y    </option></select>   </body>'),
    ('<body> <select a> <option>   X    '
     '<option> Y </option></select> </body>'),
  ),
  'colgroup_self_close': (
    '<body>  <table>  <colgroup pre>   </table></body>',
    '<body> <table> <colgroup>   </table></body>',
  ),
  'tbody_self_close': (
    ('<body>  <table>   <tbody pre>  <tr>  <td> X  </td></tr>  \n'
     '\n  <tbody>   <tr>   <td>Y   </td></tr>\n\n\n   </body>'),
    ('<body> <table> <tbody>  <tr>  <td> X  </td></tr>  \n'
     '\n  <tbody> <tr> <td>Y </td></tr> </body>'),
  ),
  'thead_self_close': (
    ('<body>  <table>   <thead pre>  <tr>  <td> X  </td></tr>  '
     '  <tbody>   <tr>   <td>Y   </td></tr> </body>'),
    ('<body> <table> <thead>  <tr>  <td> X  </td></tr>  '
     '  <tbody> <tr> <td>Y </td></tr> </body>'),
  ),
  'tfoot_self_close': (
    ('<body>  <table>   <tfoot pre>  <tr>  <td> X  </td></tr>  '
     '  <tbody>   <tr>   <td>Y   </td></tr> </body>'),
    ('<body> <table> <tfoot>  <tr>  <td> X  </td></tr>  '
     '  <tbody> <tr> <td>Y </td></tr> </body>'),
  ),
  'tr_self_close': (
    ('<body>  <table>   <thead>  <tr pre >  <td> X  </td>  '
     '    <tr>   <td>Y   </td> </body>'),
    ('<body> <table> <thead> <tr>  <td> X  </td>  '
     '    <tr> <td>Y </td> </body>'),
  ),
  'td_self_close': (
    '<body>  <table>   <thead>  <tr>  <td  pre> X       <td>Y    </body>',
    '<body> <table> <thead> <tr> <td> X       <td>Y </body>',
  ),
  'th_self_close': (
    '<body>  <table>   <thead>  <tr>  <th pre> X        <th>Y    </body>',
    '<body> <table> <thead> <tr> <th> X        <th>Y </body>',
  ),
  'a_p_interaction': ( # the 'pre' functionality continues after the </a>
    '<body><a>   <p pre>  X  </a>    <p>   Y</body>',
    '<body><a> <p>  X  </a>    <p> Y</body>',
  ),
}

SELF_OPENING_TEXTS = {
  'html_closed_no_open': (
    '<head></head><body>  X  </body></html>',
    '<head></head><body> X </body></html>'
  ),
  'head_closed_no_open': (
    '    </head><body>  X  </body>',
    ' </head><body> X </body>' # TODO: we could theoretically kill that leading
                               # space. See HTMLMinParse.handle_endtag
  ),
  'body_closed_no_open': (
    '   X  </body>',
    ' X </body>'
  ),
  'colgroup_self_open': (
    '<body>  <table>  </colgroup>   </table></body>',
    '<body> <table> </colgroup> </table></body>',
  ),
  'tbody_self_open': (
    '<body>  <table>  </tbody>   </table></body>',
    '<body> <table> </tbody> </table></body>',
  ),
  'p_closed_no_open': ( # this isn't valid html, but its worth accounting for
    '<body><div pre>   X  </p>   </div><div>    Y   </p>  </div></body>',
    '<body><div>   X  </p>   </div><div> Y </p> </div></body>',
  ),
}

class HTMLMinTestMeta(type):
  def __new__(cls, name, bases, dct):
    def make_test(text):
      def inner_test(self):
        self.assertEqual(self.minify(text[0]), text[1])
      return inner_test

    for k, v in dct.get('__reference_texts__',{}).iteritems():
      if 'test_'+k not in dct:
        dct['test_'+k] = make_test(v)
    return type.__new__(cls, name, bases, dct)

class HTMLMinTestCase(unittest.TestCase):
  __metaclass__ = HTMLMinTestMeta
  def setUp(self):
    self.minify = htmlmin.minify

class TestMinifyFunction(HTMLMinTestCase):
  __reference_texts__ = MINIFY_FUNCTION_TEXTS

  def test_basic_minification_qualify(self):
    import codecs
    inp = codecs.open('tests/large_test.html', encoding='utf-8').read()
    out = self.minify(inp)
    self.assertEqual(len(inp) - len(out), 796)

  def test_high_minification_qualify(self):
    import codecs
    inp = codecs.open('tests/large_test.html', encoding='utf-8').read()
    out = self.minify(inp, remove_empty_space=True, remove_comments=True)
    self.assertEqual(len(inp) - len(out), 4033)

class TestMinifierObject(HTMLMinTestCase):
  __reference_texts__ = MINIFY_FUNCTION_TEXTS

  def setUp(self):
    HTMLMinTestCase.setUp(self)
    self.minifier = htmlmin.Minifier()
    self.minify = self.minifier.minify

  def test_reuse(self):
    text = self.__reference_texts__['simple_text']
    self.assertEqual(self.minify(text[0]), text[1])
    self.assertEqual(self.minify(text[0]), text[1])

  def test_buffered_input(self):
    text = self.__reference_texts__['long_text']
    self.minifier.input(text[0][:len(text[0]) // 2])
    self.minifier.input(text[0][len(text[0]) // 2:])
    self.assertEqual(self.minifier.finalize(), text[1])

class TestMinifyFeatures(HTMLMinTestCase):
  __reference_texts__ = FEATURES_TEXTS

  def test_remove_comments(self):
    text = self.__reference_texts__['remove_comments']
    self.assertEqual(htmlmin.minify(text[0], remove_comments=True), text[1])

  def test_keep_comments(self):
    text = self.__reference_texts__['keep_comments']
    self.assertEqual(htmlmin.minify(text[0], remove_comments=True), text[1])

  def test_keep_pre(self):
    text = self.__reference_texts__['keep_pre']
    self.assertEqual(htmlmin.minify(text[0], keep_pre=True), text[1])

  def test_keep_empty(self):
    text = self.__reference_texts__['keep_empty']
    self.assertEqual(htmlmin.minify(text[0]), text[1])

  def test_remove_empty(self):
    text = self.__reference_texts__['remove_empty']
    self.assertEqual(htmlmin.minify(text[0], remove_empty_space=True), text[1])

  def test_dont_minify_div(self):
    text = self.__reference_texts__['dont_minify_div']
    self.assertEqual(htmlmin.minify(text[0], pre_tags=('div',)), text[1])

  def test_minify_pre(self):
    text = self.__reference_texts__['minify_pre']
    self.assertEqual(htmlmin.minify(text[0], pre_tags=('div',)), text[1])

  def test_remove_head_spaces(self):
    text = self.__reference_texts__['remove_head_spaces']
    self.assertEqual(htmlmin.minify(text[0]), text[1])

  def test_dont_minify_scripts_or_styles(self):
    text = self.__reference_texts__['dont_minify_scripts_or_styles']
    self.assertEqual(htmlmin.minify(text[0], pre_tags=[]), text[1])

  def test_in_head(self):
    text = self.__reference_texts__['in_head']
    self.assertEqual(htmlmin.minify(text[0], in_head=True), text[1])

class TestSelfClosingTags(HTMLMinTestCase):
  __reference_texts__ = SELF_CLOSE_TEXTS

class TestSelfOpeningTags(HTMLMinTestCase):
  __reference_texts__ = SELF_OPENING_TEXTS

if __name__ == '__main__':
  unittest.main()
