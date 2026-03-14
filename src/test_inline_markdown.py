from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images

def test_split():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    print("Nodes found:")
    for n in new_nodes:
        print(f"Text: '{n.text}', Type: {n.text_type}")

test_split()