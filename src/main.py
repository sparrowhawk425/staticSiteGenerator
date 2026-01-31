import os
import shutil
import sys

from textnode import TextNode, TextType
from functions.textnodemanip import markdown_to_html_node, extract_title

def copy_files_from_directory_r(source, destination):
    if not os.path.exists(source):
        raise ValueError(f"Cannot find path {source}")
    if not os.path.exists(destination):
        raise ValueError(f"Cannot find path {destination}")
    shutil.rmtree(destination)
    os.mkdir(destination)
    files = os.listdir(source)
    for file in files:
        file_path = os.path.join(source, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination)
        if os.path.isdir(file_path):
            dest_path = os.path.join(destination, file)
            os.mkdir(dest_path)
            copy_files_from_directory_r(file_path, dest_path)

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_md = ""
    html_page = ""
    with open(from_path) as from_file:
        from_md = from_file.read()
    if from_md == "":
        raise Exception(f"Failed to read contents of {from_path}")
    with open(template_path) as template_file:
        html_page = template_file.read()
    if html_page == "":
        raise Exception(f"Failed to read contents of {template_path}")
    
    html = markdown_to_html_node(from_md).to_html()
    title = extract_title(from_md)
    html_page = html_page.replace("{{ Title }}", title).replace("{{ Content }}", html)
    html_page = html_page.replace('href="', f'href="{basepath}').replace('href=', f'href="{basepath}')
    # create the destination file (create directories if they don't exist)
    print(f"Writing to file {dest_path}")
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "" and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as dest_file:
        dest_file.write(html_page)

def generate_pages_r(basepath, dir_path_content, template_path, dest_dir_path):
    content_files = os.listdir(dir_path_content)
    for content_file in content_files:
        file_path = os.path.join(dir_path_content, content_file)
        if os.path.isfile(file_path):
            print(f"generating content from {file_path}")
            generate_page(basepath, file_path, template_path, os.path.join(dest_dir_path, content_file.replace(".md", ".html")))
        if os.path.isdir(file_path):
            print(f"destination directory {dest_dir_path}")
            print(f"directory name {content_file}")
            dest_path = os.path.join(dest_dir_path, content_file)
            print(f"Generating directory {dest_path}")
            os.mkdir(dest_path)
            generate_pages_r(basepath, file_path, template_path, dest_path)

def main():
    args = sys.argv
    basepath = "/" if len(args) < 2 else args[1]

    copy_files_from_directory_r("static", "docs")
    generate_pages_r(basepath, "content", "template.html", "docs")

if __name__ == "__main__":
    main()