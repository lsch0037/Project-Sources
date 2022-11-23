class Compound:
    def __init__(self):
        self.children = []

    # node: the node or subtree to be added to the current tree
    # material: the material or list of materials to be used
    # method: "Fill", "Replace"
    def __add__(self, node, material, method="Fill"):
        pass

    # def sub(self, node):
    #     pass

    def transform(self, vector, node):
        pass

    def set(self):
        pass

class OperationNode(Compound):
    # Add(Compound, Compound)
    # Subtract(Compound, Compound)
    # Transform(Compound)
    def __init__(self, operation):
        super.__init__(self)
        self.operation = operation
    
#THIS WILL EVENTUALLY BE REPLACED BY THE PRIMITIVE DATA TYPE ITSELF
class PrimitiveNode(Compound):
    def __init__(self, shape):
        super.__init__(self)
        self.shape = shape
