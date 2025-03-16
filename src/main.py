from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType


def main():
    node = TextNode("hello", TextType.ITALIC, "https://github.com")
    html_node = HTMLNode(
        tag="a",
        value="BootDev Website",
        props={"href": "https://www.boot.dev/", "target": "_blank"},
    )

    print(
        f"<{html_node.tag}{html_node.props_to_html()}>{html_node.value}</{html_node.tag}>"
    )
    print(html_node)

    leaf = LeafNode(value="This is a paragraph", tag="p")
    print(leaf.to_html())

main()
