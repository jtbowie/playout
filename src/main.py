from htmlnode import HTMLNode
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


main()
