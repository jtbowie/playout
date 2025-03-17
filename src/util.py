import re

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


def extract_markdown(text, type="links"):
    if type == "images":
        matches = re.findall(r"!\[([^\]]+)\W+([^\)]+)", text)
    else:
        matches = re.findall(r"[^!]\[([^\]]+)\]\(([^)]+)\)", text)

    return matches


def parse_matches(matches, node, type="links"):
    start = 0
    new_node = []

    for match in matches:
        if type == "images":
            token = f"![{match[0]}]({match[1]})"
        else:
            token = f"[{match[0]}]({match[1]})"

        try:
            token_start = node.text.index(token)
        except Exception as e:
            raise ValueError(f"{e}: Could not find {token} in {node.text}")

        new_node.append(TextNode(node.text[start:token_start], TextType.TEXT))
        new_node.append(TextNode(match[0], TextType.IMAGE, match[1]))

        print("Start: ", start, "Token: ", token, "Token Start: ", token_start)
        start = token_start + len(token) + 1

    print("Start: ", start, "Len: ", len(node.text))

    if start < len(node.text) - 1:
        new_node.append(TextNode(node.text[start:], TextType.TEXT))

    return new_node


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            raise ValueError("TextNode not TEXT Node!")
        matches = extract_markdown(node.text, "images")
        if not len(matches):
            return node
        new_nodes.append(parse_matches(matches, node, "images"))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            raise ValueError("TextNode not TEXT Node!")
        matches = extract_markdown(node.text, "links")
        if not len(matches):
            return node
        new_nodes.append(parse_matches(matches, node, "links"))

    return new_nodes
