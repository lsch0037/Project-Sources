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

    def set(self):
        newBuf = buffer()

        for child in self.children:
            buf = child.set()
            buf.write(newBuf)

        return newBuf


    def unset(self):
        newBuf = buffer()

        for child in self.children:
            buf = child.unset()
            buf.write(newBuf)

        return newBuf


class differenceNode(compound):
    def set(self):
        newBuf = buffer()
        buf = self.children[0].set()
        newBuf.write(buf)

        for i in range(1,len(self.children)):
            buf = self.children[i].unset()
            newBuf.unwrite(buf)

        return newBuf

    
    def unset(self):
        newBuf = buffer()

        buf = self.children[0].unset()
        newBuf.unwrite(buf)
    
        for i in range(1,len(self.children)):
            buf = self.children[i].set()
            newBuf.write(buf)

        return newBuf


class intersectionNode(compound):
    # TODO: IMPLEMENT
    pass

class onNode(compound):
    def set(self,buf):
        first_buffer = buffer()
        second_buffer = buffer()

