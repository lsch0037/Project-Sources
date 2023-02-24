class compound():
    def __init__(self):
        self.children = []

    def addChild(self,child):
        self.children.append(child)

    def getChild(self, index):
        return self.children[index]

    # Adds addition node as parent and node as sibling
    def __add__(self, node):
        addNode = unionNode()
        addNode.addChild(self)
        addNode.addChild(node)
        
        return addNode

    # Adds subtraction node as parent and node as sibling
    def __sub__(self, node):
        subNode = differenceNode()
        subNode.addChild(self)
        subNode.addChild(node)
        
        return subNode

    def set(self, buffer):
        for child in self.children:
            child.set(buffer)

class unionNode(compound):
    # ? EXPLORE HAVING MORE THAN 2 CHILDREN

    def set(self, buffer):
        for child in self.children:
            child.set(buffer)

    def carve(self, buffer):
        for child in self.children:
            child.carve(buffer)

class differenceNode(compound):
    # ?EXPLORE HAVING MORE THAN 2 CHILDREN

    def set(self, buffer):
        self.children[0].set(buffer)
        self.children[1].carve(buffer)

    def carve(self,buffer):
        self.children[0].carve(buffer)
        self.children[1].set(buffer)

class intersectionNode(compound):
    # ? EXPLORE HAVING MORE THAN 2 CHILDREN
    pass