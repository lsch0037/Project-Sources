from pcglib.buffer import buffer

class compound():
    def __init__(self,children = []):
        self.children = children

    def addChild(self,child):
        self.children.append(child)

    def getChild(self, index):
        return self.children[index]

    # Adds addition node as parent and node as sibling
    def union(self, other):
        # addNode = unionNode()
        # addNode.addChild(self)
        # addNode.addChild(other)
        
        # return addNode

        return unionNode([self,other])

    # Adds subtraction node as parent and node as sibling
    def difference(self, other):
        # subNode = differenceNode()
        # subNode.addChild(self)
        # subNode.addChild(other)
        
        # return subNode
        return differenceNode([self,other])

    def intersection(self, other):
        subNode = differenceNode()
        # subNode.addChild(self)
        # subNode.addChild(other)
        
        return subNode


    def top(self,other):
        node = prepositionNode(buffer.getTop)
        node.addChild(self)
        node.addChild(other)

        return node

    def under(self,other):
        node = prepositionNode(buffer.getBottom)
        node.addChild(self)
        node.addChild(other)

        return node

    def inside(self,other):
        node = prepositionNode(buffer.getCenter)
        node.addChild(self)
        node.addChild(other)

        return node

    def east(self,other):
        node = prepositionNode(buffer.getEast)
        node.addChild(self)
        node.addChild(other)

        return node

    def south(self,other):
        node = prepositionNode(buffer.getSouth)
        node.addChild(self)
        node.addChild(other)

        return node

    def west(self,other):
        node = prepositionNode(buffer.getWest)
        node.addChild(self)
        node.addChild(other)

        return node

    def north(self,other):
        node = prepositionNode(buffer.getNorth)
        node.addChild(self)
        node.addChild(other)

        return node

    def offset(self,other, offset):
        node = offsetNode(offset)
        node.addChild(self)
        node.addChild(other)

        return node



    def set(self,pos,rot, buf):
        # raise ValueError("Cannot call 'set' on generic node")
        for child in self.children:
            child.set(buf,pos,rot)

    def unset(self,pos,rot,buf):
        # raise ValueError("Cannot call 'unset' on generic node")
        for child in self.children:
            child.unset(buf,pos,rot)


class unionNode(compound):
    def set(self,pos,rot):
        newBuf = buffer()

        for child in self.children:
            buf = child.set(pos,rot)
            buf.write(newBuf)

        return newBuf


    def unset(self,pos,rot):
        newBuf = buffer()

        for child in self.children:
            buf = child.unset(pos, rot)
            buf.write(newBuf)

        return newBuf


class differenceNode(compound):
    def set(self,pos,rot):
        newBuf = buffer()
        buf = self.children[0].set(pos,rot)
        newBuf.write(buf)

        for i in range(1,len(self.children)):
            buf = self.children[i].set(pos,rot)
            newBuf.unwrite(buf)

        return newBuf

    
    def unset(self,pos,rot):
        newBuf = buffer()

        buf = self.children[0].set(pos,rot)
        newBuf.unwrite(buf)
    
        for i in range(1,len(self.children)):
            buf = self.children[i].set(pos,rot)
            newBuf.write(buf)

        return newBuf


class intersectionNode(compound):
    # TODO: IMPLEMENT
    pass

class onGroundNode(compound):
    pass


class prepositionNode(compound):
    def __init__(self, f, children=[]):
        super().__init__(children)
        self.f = f

    def set(self,pos,rot):
        buf = buffer()

        # Write second object to buffer
        second_buffer = self.children[1].set(pos,rot)
        second_buffer.write(buf)

        # Get top of second object
        offset = self.f(second_buffer)

        # self.children[0].pos = top
        first_buffer = self.children[0].set(offset,rot)

        first_buffer.write(buf)

        return buf


class offsetNode(compound):
    def __init__(self,offset, children=[]):
        super().__init__(children)
        self.offset = offset

    def set(self,pos,rot):
        newBuf = buffer()

        buf = self.children[0].set(pos,rot)
        buf.write(newBuf)

        buf2 = self.children[1].set(pos + self.offset, rot)
        buf2.write(newBuf)

        return newBuf


    def unset(self,pos,rot):
        newBuf = buffer()

        buf = self.children[0].unset(pos,rot)
        buf.write(newBuf)

        buf2 = self.children[1].unset(pos + self.offset, rot)
        buf2.write(newBuf)

        return newBuf

