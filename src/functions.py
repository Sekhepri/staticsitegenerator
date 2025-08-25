from htmlnode import *
from textnode import *
from enum import Enum
import re


def text_node_to_html_node(text_node):
    '''
    Converts a single TextNode to a HTML LeafNode
    '''
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, None)
        case TextType.IMAGE:
            return LeafNode("img", None, {"src":text_node.url, "alt":text_node.text})
        case _:
            raise TypeError (f"{text_node.text_type} is not known or not implemented. available TextTypes: TEXT, BOLD, ITALIC, CODE, LINK and IMAGE")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    Splits a list of TextNodes into multiple TextNodes based on a delimiter.
    Used for spliting TextTypes into individual nodes.
    Eg. TextNode("This is text with a `code block` word", TextType.TEXT) -->
    [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT)
    ]
    '''
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splitted_node = node.text.split(delimiter)        
        if node.text[0] == delimiter:
            use_text_type = True
        else:
            use_text_type = False
        for text in splitted_node:
            if use_text_type:
                new_nodes.append(
                    TextNode(text, text_type)
                )
            else:
                new_nodes.append(
                    TextNode(text, TextType.TEXT)
                )
            use_text_type = not use_text_type
    return new_nodes

#Boot.dev recomends r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
def extract_markdown_images(text):
    '''
    Extracts image alt_text and url from a string. Helper function for split_nodes_images
    '''
    alt_text = re.findall(r"!\[(.*?)\]",text)
    src_img = re.findall(r"\((.*?)\)", text)
    return list(zip(alt_text, src_img))

#Boot.dev recomends: r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
def extract_markdown_links(text):
    '''
    Extracts link-text and url from a string. Helper function for split_nodes_link
    '''
    link_texst = re.findall(r"\[(.*?)\]",text)
    src_link = re.findall(r"\((.*?)\)", text) #
    return list(zip(link_texst, src_link))

def split_nodes_image(old_nodes):
    '''
    Splits all TextNodes in a list into Text and Image TextTypes (only if an IMAGE is found.)
    '''
    new_nodes = []
    for node in old_nodes:
        extracts = extract_markdown_images(node.text)
        if len(extracts) == 0:
            new_nodes.append(node)
        else:
            string_to_split = node.text
            for image_alt, image_link in extracts:
                splitted = (string_to_split.split(f"![{image_alt}]({image_link})", maxsplit=1))
                string_to_split = splitted[1]
                if splitted[0] != "":
                    new_nodes.append(TextNode(splitted[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if string_to_split != "":
                new_nodes.append(TextNode(string_to_split, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    '''
    Splits all TextNodes in a list into Text and Link TextTypes (only if a link is found.)
    '''
    new_nodes = []
    for node in old_nodes:
        extracts = extract_markdown_links(node.text)
        if len(extracts) == 0:
            new_nodes.append(node)
        else:
            string_to_split = node.text
            for link_alt, link_url in extracts:
                splitted = (string_to_split.split(f"[{link_alt}]({link_url})", maxsplit=1))
                string_to_split = splitted[1]
                if splitted[0] != "":
                    new_nodes.append(TextNode(splitted[0], TextType.TEXT))
                new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            if string_to_split != "":
                new_nodes.append(TextNode(string_to_split, TextType.TEXT))
    return new_nodes

def text_to_textnodes(markdown):
    '''
    Composition of helper-functions. Converts markdown tekst (innline) into TextNodes by TextTypes. 
    '''
    new_nodes = [TextNode(markdown, TextType.TEXT)]
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)  
    return new_nodes

def markdown_to_blocks(markdown):
    '''
    Splits raw markdown into seperate blocks
    '''
    blocks = []
    blocks = (markdown.strip().split("\n\n"))
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    '''
    Checks which BlockType a block belongs to and returns it.
    '''
    if re.findall(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    if re.findall(r"^\`{3}", markdown) and re.findall(r"\`{3}$", markdown) :
        return BlockType.CODE
    if re.findall(r"^> ", markdown):
        splitted = markdown.split("\n")
        for i in range(len(splitted)-1, -1, -1):
            if i == 0:
                return BlockType.QUOTE
            if not re.findall(r"^> ",splitted[i][0:2]):
                break
    if re.findall(r"^- ", markdown):
        splitted = markdown.split("\n")
        for i in range(len(splitted)-1, -1, -1):
            if i == 0:
                return BlockType.UNORDERED_LIST
            if not re.findall(r"^- ", splitted[i][0:2]):
                break
    if re.findall(r"^\d+. ", markdown):
        splitted = markdown.split("\n")
        for i in range(len(splitted)-1, -1, -1):
            if i == 0:
                return BlockType.ORDERED_LIST
            if int(splitted[i][0]) != i+1:
                break
    return BlockType.PARAGRAPH

def text_to_children(text):
    '''
    Converts text into a list of HTMLNodes
    '''
    innline_nodes = text_to_textnodes(text)
    print(innline_nodes)


def markdown_to_html_node(markdown):
    '''
    Converts a full markdown document into a single parent HTMLNode with children ending in LeafNodes.
    '''
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = ""
        match block_type:
            case BlockType.PARAGRAPH:
                tag = "p"
                nodes.append(HTMLNode(tag, block, None, None))
            case BlockType.HEADING:
                tag = "h"
                nodes.append(HTMLNode(tag, block, None, None))
            case BlockType.CODE:
                tag = "code"
                nodes.append(HTMLNode(tag, block, None, None))
            case BlockType.QUOTE:
                tag = "blockquote"
                nodes.append(HTMLNode(tag, block, None, None))
            case BlockType.UNORDERED_LIST:
                tag = "ul"
                nodes.append(HTMLNode(tag, block, None, None))
            case BlockType.ORDERED_LIST:
                tag = "ol"
                nodes.append(HTMLNode(tag, block, None, None))
            case _:
                raise Exception ("BlockType not known")
    for node in nodes:
        text_to_children(node.value)
    return nodes
            
markdown = ("""
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
This is text that _should_ remain
the **same** even with inline stuff
```
""")
nodes = markdown_to_html_node(markdown)
print(nodes)