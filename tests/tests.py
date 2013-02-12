import unittest

import htmlmin

REFERENCE_TEXTS = {
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
      "ensure that any C extensions are built. ")  # trailing whitespace
  ),
  'simple_html': (
    ' <b>  a <i pre>b  </i><pre>   x </pre>',  # <b> is not closed
    ' <b> a <i>b  </i><pre>   x </pre>'
  )
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

if __name__ == '__main__':
  unittest.main()