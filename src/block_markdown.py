from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
import re
from enum import Enum

class BlockType (Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST  = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(text):
    #HEADINGS:
    if(text[0:1] == "#"):
        heading_str = text.split(" ", 1)[0]
        
        if 1 <= len(heading_str) <= 6 and all(c == "#" for c in heading_str):
            return BlockType.HEADING
    
    #CODE BLOCKS
    if(text[0:4] == "```\n") and (text[-3:] == "```"):
        return BlockType.CODE
    
    #QUOTE BLOCKS
    if(text.startswith(">")):
        quote_lines = text.split("\n")
        fail = False
        for line in quote_lines:
            if not line.startswith(">"):
                fail = True
        if fail == False:
            return BlockType.QUOTE
    
    #UNORDERED LIST BLOCKS
    if(text[0:2] == "- "):
        unordered_list_lines = text.split("\n")
        fail = False
        for line in unordered_list_lines:
            if line[0:2] != "- ":
                fail = True
                break
        if fail == False:
            return BlockType.UNORDERED_LIST
    
    #ORDERED_LIST BLOCKS
    if(text.startswith("1. ")):
        ordered_list_lines = text.split("\n")
        fail= False
        for i in range(len(ordered_list_lines)):
            line = ordered_list_lines[i]
            if not line.startswith(f"{i+1}. "):
                fail = True 
                break
        if fail == False: 
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    result = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    # remove the "> " or ">" from each line
                    new_lines.append(line.lstrip(">").strip())
                content = " ".join(new_lines)
                children = text_to_children(content)
                node = ParentNode("blockquote", children) # Using ParentNode since it has children
                result.append(node)

            case BlockType.UNORDERED_LIST:
                li_nodes = []
                lines = block.split("\n")
                for line in lines:
                    # Strip the "- " (two characters) from the start
                    content = line[2:] 
                    # Get the inline nodes for this specific list item
                    children = text_to_children(content)
                    # Create the <li> node and add it to our list
                    li_nodes.append(ParentNode("li", children))
                
                # Now, the <ul> just takes all the <li> nodes as its children!
                node = ParentNode("ul", li_nodes)
                result.append(node)
                
            case BlockType.ORDERED_LIST:
                li_nodes = []
                lines = block.split("\n")
                for line in lines:
                    content = re.sub(r"^\d+\.\s+", "", line)
                    children = text_to_children(content)
                    li_nodes.append(ParentNode("li", children))
                node = ParentNode("ol", li_nodes)
                result.append(node)

            case BlockType.CODE:
                content = block.strip("`").strip()
                code_text_node = TextNode(content, TextType.TEXT)
                code_html_node = text_node_to_html_node(code_text_node)

                code_node = ParentNode("code", [code_html_node])
                pre_node = ParentNode("pre", [code_node])

                result.append(pre_node)

            case BlockType.HEADING:
                original_length = len(block)
                content = block.lstrip("#")
                new_length = len(content)
                heading_length = original_length - new_length
                content_strip = content.strip()
                children = text_to_children(content_strip)


                heading_node = ParentNode(f"h{heading_length}", children)
                
                result.append(heading_node)
            
            case _:
                content = block.replace("\n", " ")
                children = text_to_children(content)

                node = ParentNode("p", children)
                result.append(node)

    div_node = ParentNode("div", result)
    return div_node
            
        




#Your <ul> node should have a list of ParentNode("li", children_of_this_line) as its children.
                    #For each line in your new_lines, you'll want to call text_to_children(line) to get 
                    #the inline nodes for that specific list item.

def text_to_children(text):

    text_nodes = text_to_textnodes(text)

    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        new_block = block.strip()
        if(new_block == ""):
            continue
        result.append(new_block)
    return result