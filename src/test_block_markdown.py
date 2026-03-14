from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images
import re
import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from enum import Enum

class TestMarkdownBlocks(unittest.TestCase):
    def test_block_to_block_type(self):
        # 1. Test Heading
        block = "# this is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        # 2. Test Code
        block = "```\nthis is code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # 3. Test Quote
        block = "> this is a quote\n> with two lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        # 4. Test Unordered List
        block = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        # 5. Test Ordered List
        block = "1. first\n2. second"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        # 6. Test Paragraph (The catch-all)
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
if __name__ == "__main__":
    unittest.main()


def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )


def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )