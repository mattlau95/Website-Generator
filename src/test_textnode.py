import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        #tests that two nodes with identical properties are equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        #Test that nodes with URLs are equal
        node = TextNode("This is a text node", "italic", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "italic", "https://www.boot.dev")
        self.assertEqual(node, node2)
    
    def test_not_eq_text(self):
        #test that nodes with same text are NOT rqual
        node = TextNode("This is text node", TextType.BOLD)
        node2 = TextNode("Tis' a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
