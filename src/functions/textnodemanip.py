import re

from enum import Enum
from functools import reduce

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            pass

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if delimiter == "":
        raise ValueError("Cannot have empty delimiter")
    for node in old_nodes:
        # only process text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        # If we have an even number of delimiters, we should have an odd number of sections
        if len(sections) % 2 == 0:
            raise Exception(f"Invalid markdown format: missing delimiter ({delimiter})")
        count = 0
        def wrapper(s):
            n = None
            nonlocal count
            if count % 2 == 0:
                n = TextNode(s, TextType.TEXT)
            else:
                n = TextNode(s, text_type)
            count += 1
            return n
        new_nodes.extend(filter(lambda n: n.text != "", map(wrapper, sections)))
    return new_nodes

# extract list of tuples of format ![tup0](tup1)
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# extract list of tuples of format [tup0](tup1)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        # if there were no images just add the node as-is
        if images == []:
            new_nodes.append(node)
            continue
        sections = node.text
        for img in images:
            sections = sections.split(f"![{img[0]}]({img[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            sections = sections[1]
        if sections != "":
            new_nodes.append(TextNode(sections, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        # if there were no links just add the node as-is
        if links == []:
            new_nodes.append(node)
            continue
        sections = node.text
        for link in links:
            sections = sections.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            sections = sections[1]
        if sections != "":
            new_nodes.append(TextNode(sections, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    return list(filter(lambda b: b != "", map(lambda b: b.strip(), markdown.split("\n\n"))))

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    # headings start with 1-6 # and a space
    if re.match(r"#{1,6} ", block) is not None:
        return BlockType.HEADING
    
    # code block starts with ```\n and ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    # quotes: every line starts with >
    lines = block.split("\n")
    is_quote = reduce(lambda a, b: a and b, map(lambda l: l.startswith(">"), lines))
    if is_quote:
        return BlockType.QUOTE
        
    # unordered list: starts with '- '
    is_unordered = reduce(lambda a, b: a and b, map(lambda l: l.startswith("- "), lines))
    if is_unordered:
        return BlockType.UNORDERED_LIST

    # ordered list: starts with numbers (from 1, incrementing) plus '. '
    is_ordered = True
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            is_ordered = False
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    # regular paragraph
    return BlockType.PARAGRAPH

def text_to_children(tag, value):
    text_nodes = text_to_textnodes(value)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode(tag, html_nodes)

def create_header_node(text):
    count = 0
    for c in text:
        if c == "#":
            count += 1
        if c == " ":
            break
    if count > 6:
        count = 6
    return text_to_children(f"h{count}", text[count + 1:])

def create_code_node(text):
    return ParentNode("pre", [LeafNode("code", text.strip("`\n"))])

def create_blockquote_node(text):
    unformatted_text = text.strip("> ").replace("\n>", "")
    return text_to_children("blockquote", unformatted_text)

def create_list_item_node(text):
    return text_to_children("li", text)

def create_unordered_list_node(text):
    lines = text.split("- ")
    nodes = []
    for line in lines:
        line = line.strip()
        if line != "":
            nodes.append(create_list_item_node(line))
    return ParentNode("ul", nodes)

def create_ordered_list_node(text):
    lines = re.split(r"[0-9]+\. ", text)
    nodes = []
    for line in lines:
        line = line.strip()
        if line != "":
            nodes.append(create_list_item_node(line))
    return ParentNode("ol", nodes)

def create_paragraph_node(text):
    return text_to_children("p", text.replace("\n", " "))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING: # <h?>
                nodes.append(create_header_node(block))
            case BlockType.CODE: # <pre><code>
                nodes.append(create_code_node(block))
            case BlockType.QUOTE: # <blockquote>
                nodes.append(create_blockquote_node(block))
            case BlockType.UNORDERED_LIST: # <ul><li>
                nodes.append(create_unordered_list_node(block))
            case BlockType.ORDERED_LIST: # <ol><li>
                nodes.append(create_ordered_list_node(block))
            case BlockType.PARAGRAPH: # <p>
                nodes.append(create_paragraph_node(block))
    return ParentNode("div", nodes)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("markdown does not have title header")