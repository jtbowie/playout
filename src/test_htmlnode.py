import unittest

from htmlnode import HTMLNode


class TestiHTMLNode(unittest.TestCase):

    def test_eq(self):
        html_node = HTMLNode(
            value="BootDev Super Awesome website!",
            props={"href": "https://boot.dev/"},
            tag="a",
        )
        self.assertEqual(html_node.props_to_html(), ' href="https://boot.dev/" ')


if __name__ == "__main__":
    unittest.main()
