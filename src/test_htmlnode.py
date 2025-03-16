import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from util import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_by_markdown,
    text_node_to_htmlnode,
)


class TestiHTMLNode(unittest.TestCase):

    def test_eq(self):
        html_node = HTMLNode(
            value="BootDev Super Awesome website!",
            props={"href": "https://boot.dev/"},
            tag="a",
        )
        self.assertEqual(html_node.props_to_html(), ' href="https://boot.dev/" ')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a", "https://www.boot.dev/", props={"href": "https://boot.dev/"}
        )
        self.assertEqual(
            node.to_html(), '<a href="https://boot.dev/" >https://www.boot.dev/</a>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_htmlnode(node)
        if not html_node:
            raise Exception("Node is not a HTMLNode")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image_text_node_to_htmlnode(self):
        node = TextNode(
            "This is an image", TextType.IMAGE, url="https://boot.dev/icon.png"
        )
        html_node = text_node_to_htmlnode(node)
        if not html_node:
            raise Exception("Node is not a HTMLNode")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], node.url)

    def test_link_text_node_to_htmlnode(self):
        node = TextNode("BootDev Inc", TextType.LINK, url="https://boot.dev/")
        html_node = text_node_to_htmlnode(node)
        if not html_node:
            raise Exception("Node is not a HTMLNode")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, node.text)
        self.assertEqual(html_node.props["href"], node.url)

    def test_markdown_textnode_parser(self):
        node = TextNode("This is *bold* text!!", TextType.TEXT)
        markdown_node = split_nodes_by_markdown([node], "*", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text!!", TextType.TEXT),
            ],
            markdown_node,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is my link! [this is my link](https://www.boot.dev/) Thank you!"
        )
        self.assertListEqual([("this is my link", "https://www.boot.dev/")], matches)


if __name__ == "__main__":
    unittest.main()
