import unittest

from htmlnode import HTMLNode, LeafNode


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
        node = LeafNode("a", "https://www.boot.dev/", props={'href': 'https://boot.dev/'})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev/" >https://www.boot.dev/</a>')

if __name__ == "__main__":
    unittest.main()
