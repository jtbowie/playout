import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from util import (
    extract_markdown,
    markdown_to_blocks,
    split_nodes_by_markdown,
    split_nodes_image,
    split_nodes_link,
    text_node_to_htmlnode,
    text_to_textnodes,
)


class TestHTMLNode(unittest.TestCase):

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

    def test_markdown_textnode_no_tail(self):
        node = TextNode("This is *BOLD*", TextType.TEXT)
        markdown_node = split_nodes_by_markdown([node], "*", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
            ],
            markdown_node,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", "images"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown(
            "This is my link! [this is my link](https://www.boot.dev/) Thank you!",
            "links",
        )
        self.assertListEqual([("this is my link", "https://www.boot.dev/")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):

        text = (
            "This is **text** with an _italic_ word and a `code block`"
            " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )

        test_output = text_to_textnodes(text)

        print("============ text_to_textnodes =============")
        print(test_output)
        print("============================================")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            test_output,
        )

    def test_markdown_to_block(self):
        md = """
    This is **bolded** paragraph
    
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    
    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)

        print("============ markdown_to_blocks =============")
        print(blocks)
        print("=============================================")

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_block_mmultiple_blank_lines(self):
        md = """
        This block should be one line

        This block should be
        two lines


        This block
        Should be
        Three lines



        There should be four blocks.
        """

        blocks = markdown_to_blocks(md)

        print("============ markdown_to_blocks =============")
        print(blocks)
        print("=============================================")

        self.assertEqual(
            blocks,
            [
                "This block should be one line",
                "This block should be\ntwo lines",
                "This block\nShould be\nThree lines",
                "There should be four blocks.",
            ],
        )


if __name__ == "__main__":
    unittest.main()
