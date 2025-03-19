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


def make_nodes(working_set, output, text_type):
    while working_set:
        node_list = [
            TextNode(working_set.pop(), TextType.TEXT),
            TextNode(working_set.pop(), text_type),
            TextNode(working_set.pop(), TextType.TEXT),
        ]

        if not node_list[2].text:
            node_list.pop()

        output.extend(node_list)


def split_nodes_by_markdown(old_nodes, delimiter, text_type):
    output = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue

        working_set = node.text.split(delimiter)
        working_set_len = len(working_set)

        if working_set_len < 3:
            for item in working_set:
                output.append(TextNode(item, TextType.TEXT))
            continue

        working_set.reverse()

        if working_set_len > 2 and not working_set_len % 2:
            raise Exception("This is not valid markdown syntax")

        make_nodes(working_set, output, text_type)

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
        if type == "images":
            new_node.append(TextNode(match[0], TextType.IMAGE, match[1]))
        else:
            new_node.append(TextNode(match[0], TextType.LINK, match[1]))

        start = token_start + len(token)

    if start < len(node.text) - 1:
        new_node.append(TextNode(node.text[start:], TextType.TEXT))

    return new_node


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown(node.text, "images")
        if not len(matches):
            new_nodes.append(node)
            continue
        new_nodes.extend(parse_matches(matches, node, "images"))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown(node.text, "links")
        if not len(matches):
            new_nodes.append(node)
            continue
        new_nodes.extend(parse_matches(matches, node, "links"))

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_by_markdown([node], "**", TextType.BOLD)
    nodes = split_nodes_by_markdown(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_by_markdown(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes


def markdown_to_blocks(markdown):
    output = []
    block = []

    scratchpad = markdown.split("\n")
    for line in scratchpad:
        line = line.strip()
        if not line:
            if len(block):
                output.append("\n".join(block))
                block = []
        else:
            print(f'line = "{line}"')
            block.append(line)

    if block:
        output.append("\n".join(block))

    return output
