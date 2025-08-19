from htmlnode import *
from textnode import *
import re

def text_node_to_html_node(text_node):
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
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
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
    alt_text = re.findall(r"!\[(.*?)\]",text)
    src_img = re.findall(r"\((.*?)\)", text)
    return list(zip(alt_text, src_img))

#Boot.dev recomends: r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
def extract_markdown_links(text):
    link_texst = re.findall(r"\[(.*?)\]",text)
    src_link = re.findall(r"\((.*?)\)", text) #
    return list(zip(link_texst, src_link))
