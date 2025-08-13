

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
        for key, value in self.props.items():
            new_string += f'{key}="{value}" '
        new_string = new_string.rstrip()
        return new_string
    def __repr__(self):
        debug_string = f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"
        return debug_string
    
    def __eq__(self, other):    #for unit-tests
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
