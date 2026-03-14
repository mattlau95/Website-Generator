import unittest
from main import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        actual = extract_title(markdown)
        expected = "Hello"
        self.assertEqual(actual, expected)

    def test_extract_title_exception(self):
        markdown = "## No H1 here"
        # This is how we test that a specific error is raised
        with self.assertRaises(Exception):
            extract_title(markdown)