from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from util import split_nodes_by_markdown


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

    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node.to_html())

    node = TextNode("This is *bold* markdown!!", TextType.TEXT)
    output = split_nodes_by_markdown([node], "*", TextType.BOLD)
    print(output)

    node = TextNode("This is *bold markdown*!!", TextType.TEXT)
    output = split_nodes_by_markdown([node], "*", TextType.BOLD)
    print(output)

    node = TextNode("This is *bold markdown!!", TextType.TEXT)
    output = split_nodes_by_markdown([node], "*", TextType.BOLD)
    print(output)


main()
