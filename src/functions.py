from htmlnode import *
from textnode import *

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