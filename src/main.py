from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode




def main():
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    dummy2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    dummy3 = TextNode("ikke lik de andre", TextType.LINK, "https://www.boot.dev")

    print(dummy)

main()