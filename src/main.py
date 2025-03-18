from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from util import (extract_markdown, split_nodes_by_markdown, split_nodes_image,
                  text_node_to_htmlnode)


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

    node = TextNode("This is _italic_ markdown!!", TextType.TEXT)
    output = split_nodes_by_markdown([node], "_", TextType.TEXT)
    print(output)

    node = TextNode("This is *bold* and _italic_ markdown!!", TextType.TEXT)
    output = split_nodes_by_markdown([node], "*", TextType.BOLD)
    node_list = split_nodes_by_markdown([output.pop()], "_", TextType.ITALIC)
    for new_node in node_list:
        output.append(new_node)
    print(output)

    print(
        extract_markdown(
            "Test image: ![image](https://boot.dev/images/hero.png) incoming!", "images"
        )
    )
    print(
        extract_markdown(
            "Test image: ![hero-image](https://boot.dev/images/hero.png) incoming! Also test image: ![villain-image](https://boot.dev/images/villain.png)",
            "images",
        )
    )

    text_nodes = split_nodes_image(
        [
            TextNode(
                "Test image: ![hero-image](https://boot.dev/images/hero.png) incoming!  "
                "Test image2: ![vkillain-image](https://boot.dev/images/villain.png) incoming!",
                TextType.TEXT,
            )
        ]
    )

    image_html_nodes = []
    print(text_nodes)

    for node_set in text_nodes:
        for node in node_set:
            image_html_nodes.append(text_node_to_htmlnode(node))

    for tag in image_html_nodes:
        print(tag)


main()
