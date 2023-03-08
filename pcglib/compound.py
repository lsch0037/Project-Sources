from pcglib.buffer import buffer

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

    def set(self, buf):
        # raise ValueError("Cannot call 'set' on generic node")
        for child in self.children:
            child.set(buf)

    def unset(self,buf):
        # raise ValueError("Cannot call 'unset' on generic node")
        for child in self.children:
            child.unset(buf)


class unionNode(compound):

    def set(self, buf):
        newBuf = buffer()

        for child in self.children:
            child.set(newBuf)

        newBuf.write(buf)

    def unset(self, buf):
        newBuf = buffer()

        for child in self.children:
            child.unset(newBuf)

        newBuf.write(buf)

class differenceNode(compound):
    def set(self,buf):
        newBuf = buffer()
        self.children[0].set(newBuf)
    
        for i in range(1,len(self.children)):
            self.children[i].unset(newBuf)

        newBuf.write(buf)
    
    def unset(self,buf):
        newBuf = buffer()
        self.children[0].unset(newBuf)
    
        for i in range(1,len(self.children)):
            self.children[i].set(newBuf)

        newBuf.write(buf)


class intersectionNode(compound):
    # TODO: IMPLEMENT
    pass