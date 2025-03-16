from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_htmlnode(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Not a valid TextType")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text, props=None)
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": ""})
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text, props=None)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text, props=None)
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})


def split_nodes_by_markdown(old_nodes, delimiter, text_type):
    output = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue

        working_set = node.text.split(delimiter)
        working_set_len = len(working_set)

        if working_set_len < 3:
            output.append(node)
            continue

        working_set.reverse()

        if working_set_len > 2 and not working_set_len % 2:
            raise Exception("This is not valid markdown syntax")

        while working_set:
            print(len(working_set))
            node_list = [
                TextNode(working_set.pop(), TextType.TEXT),
                TextNode(working_set.pop(), text_type),
                TextNode(working_set.pop(), TextType.TEXT),
            ]
            output.extend(node_list)

    return output
