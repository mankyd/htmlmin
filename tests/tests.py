import unittest

import htmlmin

REFERENCE_TEXTS = {
  'simple_text': (
    '<body>  a  b</body>',
    '<body> a b</body>'
  ),
  'long_text': (
    '''<body>When doing     test-driven development, or
    running automated builds that need testing before they are  deployed
\t\t for downloading or use, it's often useful to be able to run a project's
unit tests without actually deploying the project anywhere.\r\n\r\n\n\r\rThe
test command runs project's unit tests without actually deploying it, by
    temporarily putting the project's source on sys.path, after first running
     build_ext -i to ensure that any C extensions are built.

    </body>  ''',
    ("<body>When doing test-driven development, or running automated "
      "builds that need testing before they are deployed for "
      "downloading or use, it's often useful to be able to run a "
      "project's unit tests without actually deploying the project "
      "anywhere. The test command runs project's unit tests without "
      "actually deploying it, by temporarily putting the project's "
      "source on sys.path, after first running build_ext -i to "
      "ensure that any C extensions are built. </body> ")  # trailing whitespace
  ),
  'simple_html': (
    ('<body> <b>  a <i pre>b  </i>'  # <b> is not closed
     '<pre>   x </pre> <textarea>   Y  </textarea></body>'),
    '<body> <b> a <i>b  </i><pre>   x </pre> <textarea>   Y  </textarea></body>'
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
    '<head>  <title> hi   </title>  </head>',
    '<head><title>hi</title></head>',
  ),
  'dont_minify_scripts_or_styles': (
    '<body>  <script>   X  </script>  <style>   X</style>   </body>',
    '<body> <script>   X  </script> <style>   X</style> </body>',
  ),
}
class TestMinifyFunction(unittest.TestCase):
  def test_simple_text(self):
    text = REFERENCE_TEXTS['simple_text']
    self.assertEqual(htmlmin.minify(text[0]), text[1])

  def test_long_text(self):
    text = REFERENCE_TEXTS['long_text']
    self.assertEqual(htmlmin.minify(text[0]), text[1])

  def test_simple_html(self):
    text = REFERENCE_TEXTS['simple_html']
    self.assertEqual(htmlmin.minify(text[0]), text[1])

class TestMinifierObject(unittest.TestCase):
  def setUp(self):
    self.minifier = htmlmin.Minifier()

  def test_simple_text(self):
    text = REFERENCE_TEXTS['simple_text']
    self.assertEqual(self.minifier.minify(text[0]), text[1])

  def test_simple_long_text(self):
    text = REFERENCE_TEXTS['long_text']
    self.assertEqual(self.minifier.minify(text[0]), text[1])

  def test_simple_html(self):
    text = REFERENCE_TEXTS['simple_html']
    self.assertEqual(self.minifier.minify(text[0]), text[1])

  def test_reuse(self):
    text = REFERENCE_TEXTS['simple_text']
    self.assertEqual(self.minifier.minify(text[0]), text[1])
    self.assertEqual(self.minifier.minify(text[0]), text[1])

  def test_buffered_input(self):
    text = REFERENCE_TEXTS['long_text']
    self.minifier.input(text[0][:len(text[0]) // 2])
    self.minifier.input(text[0][len(text[0]) // 2:])
    self.assertEqual(self.minifier.finalize(), text[1])

class TestMinifyOptions(unittest.TestCase):
  def test_remove_comments(self):
    text = REFERENCE_TEXTS['remove_comments']
    self.assertEqual(htmlmin.minify(text[0], remove_comments=True), text[1])

  def test_keep_comments(self):
    text = REFERENCE_TEXTS['keep_comments']
    self.assertEqual(htmlmin.minify(text[0], remove_comments=True), text[1])

  def test_keep_pre(self):
    text = REFERENCE_TEXTS['keep_pre']
    self.assertEqual(htmlmin.minify(text[0], keep_pre=True), text[1])

  def test_keep_empty(self):
    text = REFERENCE_TEXTS['keep_empty']
    self.assertEqual(htmlmin.minify(text[0]), text[1])

  def test_remove_empty(self):
    text = REFERENCE_TEXTS['remove_empty']
    self.assertEqual(htmlmin.minify(text[0], remove_empty_space=True), text[1])

  def test_dont_minify_div(self):
    text = REFERENCE_TEXTS['dont_minify_div']
    self.assertEqual(htmlmin.minify(text[0], pre_tags=('div',)), text[1])

  def test_minify_pre(self):
    text = REFERENCE_TEXTS['minify_pre']
    self.assertEqual(htmlmin.minify(text[0], pre_tags=('div',)), text[1])

  def test_remove_head_spaces(self):
    text = REFERENCE_TEXTS['remove_head_spaces']
    self.assertEqual(htmlmin.minify(text[0]), text[1])

  def test_dont_minify_scripts_or_styles(self):
    text = REFERENCE_TEXTS['dont_minify_scripts_or_styles']
    self.assertEqual(htmlmin.minify(text[0], pre_tags=[]), text[1])

if __name__ == '__main__':
  unittest.main()
