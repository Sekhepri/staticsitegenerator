from enum import Enum
from htmlnode import *
from textnode import *

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