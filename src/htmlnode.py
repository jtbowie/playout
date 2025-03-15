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
