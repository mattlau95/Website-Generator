from textnode import TextNode
import os
import shutil
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from enum import Enum
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, text_to_textnodes
import block_markdown
from copystatic import copy_files_recursive
from pathlib import Path

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"
    
def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception(f"Source path {dir_path_content} does not exist.")
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    items = os.listdir(dir_path_content)
    for item in items:
        new_src = os.path.join(dir_path_content, item)
        new_dest = os.path.join(dest_dir_path, item)
        print(f"Found item: {new_src}, is dir: {os.path.isdir(new_src)}, is file: {os.path.isfile(new_src)}")
        if os.path.isfile(new_src) and new_src.endswith(".md"):
            print(f"copying {new_src} from {dir_path_content} to {new_dest}.")
            dest_html = str(Path(new_dest).with_suffix(".html"))
            generate_page(new_src, template_path, dest_html)
            # generate_page(new_src, template_path, new_dest)
        elif os.path.isdir(new_src):
            generate_pages_recursive(new_src, template_path, new_dest)
    

def copy_all_contents(src, dst):
    if not os.path.exists(src):
        raise Exception(f"Sorce path {src} does not exist.")
    if not os.path.exists(dst):
        os.mkdir(dst)

    items = os.listdir(src)
    for item in items:
        new_src = os.path.join(src, item)
        new_dst = os.path.join(dst, item)
        if os.path.isfile(new_src):
            print(f"copying {new_src} from {src} to {new_dst}.")
            shutil.copy(new_src, new_dst)
        elif os.path.isdir(new_src):
            copy_all_contents(new_src, new_dst)
    
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    result = []
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block.startswith("# "):
                content = block[2:]
                return content
    raise Exception("No h1 header found.")   

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(f'{from_path}', 'r', encoding='utf-8') as file:
        from_markdown = file.read()

    title = extract_title(from_markdown)

    with open(f'{template_path}', 'r', encoding='utf-8') as file:
        template_file = file.read()

    HTML_content = (markdown_to_html_node(from_markdown)).to_html()

    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", HTML_content)

    with open(f'{dest_path}', 'w', encoding='utf-8') as file:
        file.write(template_file)




if __name__ == "__main__":
    main()
