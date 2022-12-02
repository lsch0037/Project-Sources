import ServerOperations

class Compound:
    def __init__(self):
        self.children = []

    def addChild(self,child):
        self.children.append(child)

    def getChild(self, index):
        return self.children[index]

    def transform(self, vector, node):
        pass

    # Adds addition node as parent and node as sibling
    def __add__(self, node):
        addNode = additionNode()
        addNode.addChild(self)
        addNode.addChild(node)
        
        return addNode

    # Adds subtraction node as parent and node as sibling
    def __sub__(self, node):
        subNode = subtractionNode()
        subNode.addChild(self)
        subNode.addChild(node)
        
        return subNode

class additionNode(Compound):
    def set(self):
        for child in self.children:
            child.set()

    def carve(self):
        for child in self.children:
            child.carve()

class subtractionNode(Compound):

    def set(self):
        self.children[0].set()
        self.children[1].carve()

    def carve(self):
        self.children[0].carve()
        self.children[1].set()

#THIS WILL EVENTUALLY BE REPLACED BY THE PRIMITIVE DATA TYPE ITSELF
class PrimitiveNode(Compound):
    def __init__(self, O, dim, material, replacing=-1):
        self.children = []
        self.O = O
        self.dim = dim
        self.material = material
        self.replacing = replacing

    # Sets the shape in the world
    def set(self):
        pos1 = self.O + [self.dim, self.dim, self.dim]
        ServerOperations.fill(self.O, pos1, self.material, self.replacing)

    # Sets the shape as air in the world
    def carve(self):
        pos1 = self.O + [self.dim, self.dim, self.dim]
        ServerOperations.fill(self.O, pos1, 0, self.replacing)
        
    def transform(T):
        pass