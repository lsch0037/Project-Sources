import ServerOperations

class Compound:
    def __init__(self):
        self.children = []

    def transform(self, vector, node):
        pass

    # Adds addition node as parent and node as sibling
    def add(self, node):
        pass

    # Adds subtraction node as parent and node as sibling
    def sub(self):
        pass

    # Calls the set on itself and the subtree
    def set_traverse(self):
        for child in self.children:
            child.set()

    # Calls the carve on itself and the subtree
    def carve_traverse(self):
        for child in self.children:
            child.carve()


class additionNode(Compound):
    def set_traverse(self):
        return super().set_traverse()


    def execute(self):
        for child in self.children:
            child.execute()

class subtractionNode(Compound):

    def set(self):
        self.carve()

#THIS WILL EVENTUALLY BE REPLACED BY THE PRIMITIVE DATA TYPE ITSELF
class PrimitiveNode(Compound):
    def __init__(self, O, dim, material):
        super.__init__(self)
        self.O = O
        self.dim = dim
        self.material = material

    # Sets the shape in the world
    def set(self):
        pos1 = self.O + [self.dim, self.dim, self.dim]
        ServerOperations.fill(self.O, pos1, self.material)

    # Sets the shape as air in the world
    def carve(self):
        pos1 = self.O + [self.dim, self.dim, self.dim]
        ServerOperations.fill(self.O, pos1, 0)
        
    def transform(T):
        pass