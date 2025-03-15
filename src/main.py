from textnode import TextNode, TextType


def main():
    node = TextNode("hello", TextType.ITALIC, "https://github.com")
    print(node)


main()
