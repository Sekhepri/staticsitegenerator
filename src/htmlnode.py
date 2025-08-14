

class HTMLNode():
    def __init__(self= None, tag= None, value= None, children= None, props= None):
        self.tag = tag
        self.value = value
        """
        for child in children:
            if not isinstance(child, HTMLNode):
                raise TypeError (f"{children} are not of type HTMLNode")
        """
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        new_string = ""
        if self.props == None:
            return new_string
        for key, value in self.props.items():
            new_string += f' {key}="{value}"'
        return new_string
    
    def __repr__(self):
        debug_string = f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"
        return debug_string
    
    def __eq__(self, other):    #for unit-tests
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError ("no value found. All LeafNode objects must have a value")
        if self.tag == None:
            return self.value
        props = super().props_to_html()
        html_string = f"<{self.tag}{props}>{self.value}</{self.tag}>"
        return html_string

    def __eq__(self, other):
        return super().__eq__(other)

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError ("no tag found. All ParentNode objects must have a tag")
        if self.children == None or len(self.children) < 1:
            raise ValueError ("no children found. All ParentNode objects must have one or more children")
        props = super().props_to_html()
        html_string = f"<{self.tag}{props}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string