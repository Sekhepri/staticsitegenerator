from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"       #**Bold text**
    ITALIC = "italic"   #_Italic text_
    CODE = "code"       #'Code text'
    LINK = "link"       #[anchor text](url)
    IMAGE = "image"     #![alt text](url)

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if isinstance(text_type, TextType):
            self.text_type = text_type
        else:
            raise TypeError(f"{text_type} is not a valid TextType. available types: plain, bold, italic, code, link, image")
        self.url = url
    
    def __eq__(self, other):
        return(
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
            )
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
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