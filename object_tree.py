class object_tree():
    def __init__(self):
        self.children = []

class object_node(object_tree):
    def __init__(self, object_name, descriptors=[]):
        self.object_name = object_name
        self.descriptors = descriptors

    def evaluate(self):
        # TODO RETURN THE JSON PROGRAM
        pass

class modifier_node(object_tree):
    def __init__(self, modifier, of_object_name):
        self.modifier = modifier
        self.of_object_name = of_object_name

        super().__init__(self)
    
    def evaluate(self):
        # TODO RECURSIVELY EVALUATE ALL SUBTREES
        pass