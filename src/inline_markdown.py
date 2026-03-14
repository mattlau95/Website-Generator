from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        split_old_node = old_node.text.split(delimiter)

        if len(split_old_node) % 2 == 0:
            raise Exception("Delimiters are not balanced.")
            
        for i in range(len(split_old_node)):
            if split_old_node[i] == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(split_old_node[i], TextType.TEXT))
            else:
                result.append(TextNode(split_old_node[i], text_type))
    return result

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        text = old_node.text
        if(text == ""):
            continue
        images = extract_markdown_images(text)
        if not images:
            if(text != ""):
                result.append(old_node)
                continue
        else:    
            for image in images:
                split_text = text.split(f"![{image[0]}]({image[1]})", 1)
                if split_text[0] != "":
                    result.append(TextNode(split_text[0], TextType.TEXT))
                result.append(TextNode(image[0], TextType.IMAGE, image[1]))
                text = split_text[1]
            if(text != ""):
                result.append(TextNode(text, TextType.TEXT))
    return result
                
def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        text = old_node.text
        if(text == ""):
            continue
        links = extract_markdown_links(text)
        if not links:
            if(text != ""):
                result.append(old_node)
                continue
        else:    
            for link in links:
                split_text = text.split(f"[{link[0]}]({link[1]})", 1)
                if split_text[0] != "":
                    result.append(TextNode(split_text[0], TextType.TEXT))
                result.append(TextNode(link[0], TextType.LINK, link[1]))
                text = split_text[1]
            if(text != ""):
                result.append(TextNode(text, TextType.TEXT))
    return result

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnodes(text):
    # Start with a list containing one initial TextNode
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Each function takes a list of nodes and returns a flattened list of nodes
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # Usually * or _
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)    # Backtick for code
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes










        
        
