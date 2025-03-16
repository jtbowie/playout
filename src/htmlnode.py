from textnode import TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("To be continued...")

    def props_to_html(self):
        output = ""
        if not self.props:
            raise ValueError("No props set")
        for k, v in self.props.items():
            output += f' {k}="{v}"'
        return output + " "

    def __repr__(self):
        output = "HTMLNode("
        if self.tag:
            output += f"tag={self.tag}, "
        else:
            output += "tag=None, "
        if self.value:
            output += f"value={self.value}, "
        else:
            output += "value=None, "
        if self.children:
            output += f"children={self.children}, "
        else:
            output += "children=None, "
        if self.props:
            output += f"props={self.props}, "
        else:
            output += "props=None, "
        return output[:-2] + ")"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("No value Node")
        if not self.tag:
            return self.value
        else:
            if self.props:
                return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
            return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("No tag set")

        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag set")
        if not self.children:
            raise ValueError("No children set")
        if not self.props:
            output = f"<{self.tag}>"
        else:
            output = f"<{self.tag}{super().props_to_html()}>"

        for child in self.children:
            output += child.to_html()
        return output + f"</{self.tag}>"


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
