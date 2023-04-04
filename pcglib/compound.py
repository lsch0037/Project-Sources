from pcglib.buffer import buffer

import numpy as np
import math

class compound():
    def __init__(self,children = []):
        self.children = children

    def addChild(self,child):
        self.children.append(child)

    def getChild(self, index):
        return self.children[index]

    # Adds addition node as parent and node as sibling
    def union(self, other):
        return unionNode([self,other])

    # Adds subtraction node as parent and node as sibling
    def difference(self, other):
        return differenceNode([self,other])

    def intersection(self, other):
        return intersectionNode([self,other])


    def onTopOf(self,other):
        return prepositionNode(buffer.getBottom,buffer.getTop, [self,other])

    def under(self,other):
        return prepositionNode(buffer.getTop, buffer.getBottom, [self,other])

    def insideOf(self,other):
        return prepositionNode(buffer.getCenter, buffer.getCenter, [self,other])

    def eastOf(self,other):
        return prepositionNode(buffer.getWest, buffer.getEast, [self,other])

    def southOf(self,other):
        return prepositionNode(buffer.getNorth,buffer.getSouth, [self,other])

    def westOf(self,other):
        return prepositionNode(buffer.getEast, buffer.getWest, [self,other])

    def northOf(self,other):
        return prepositionNode(buffer.getSouth, buffer.getNorth, [self,other])

    def offsetBy(self,other, offset):
        return offsetNode(offset, [self,other])


    def set(self,pos,rot, buf):
        raise ValueError("Cannot call 'set' on generic node")
        # for child in self.children:
        #     child.set(buf,pos,rot)

    def unset(self,pos,rot,buf):
        raise ValueError("Cannot call 'unset' on generic node")
        # for child in self.children:
        #     child.unset(buf,pos,rot)


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

# class onGroundNode(compound):
    # def set(self, pos,rot):
    #     groundPos = 

    #     for child in self.children:

class prepositionNode(compound):
    def __init__(self, f1, f2, children=[]):
        super().__init__(children)
        self.f1 = f1
        self.f2 = f2

    def set(self,pos,rot):
        buf = buffer()

        # Write first object to buffer
        first_buffer = self.children[0].set(pos,rot)
        # Get anchor point of second object
        pos1 = self.f1(first_buffer)

        # Write second object to buffer
        second_buffer = self.children[1].set(pos,rot)
        # Get anchor point of second object
        pos2 = self.f2(second_buffer)

        # Calculate difference between anchor points
        offset = pos2 - pos1

        # Shift to lign up anchor points
        first_buffer.shift(offset)

        # Write to final buffer
        first_buffer.write(buf)
        second_buffer.write(buf)

        return buf


class offsetNode(compound):
    def __init__(self,offset, children=[]):
        super().__init__(children)
        self.offset = offset

    def set(self,pos,rot):
        print("Pos:{p}, Offset:{o}".format(p=pos,o=self.offset))
        return self.children[0].set(np.add(pos,self.offset), rot)


    def unset(self,pos,rot):
        newBuf = buffer()

        buf = self.children[0].unset(pos,rot)
        buf.write(newBuf)

        # todo rotate offset by 'rot'

        buf2 = self.children[1].unset(pos + self.offset, rot)
        buf2.write(newBuf)

        return newBuf


class rotationNode(compound):
    def __init__(self,axis, deg, children=[]):
        super().__init__(children)

        functions = [rotateX, rotateY, rotateZ]

        self.f = functions[axis]
        self.deg = deg


    def set(self,pos,prev_rot):

        newBuf = buffer()

        new_rot = self.f(prev_rot, self.deg)

        for child in self.children:
            buf = child.set(pos, new_rot)
            buf.write(newBuf)

        return newBuf


    def unset(self,pos, prev_rot):
        newBuf = buffer()

        new_rot = self.f(prev_rot, self.deg)

        for child in self.children:
            buf = child.set(pos, new_rot)
            buf.unwrite(newBuf)

        return newBuf


def rotateX(mat, deg):

    # Type Checking
    if not isinstance(mat, (list, np.ndarray)):
        raise TypeError("Argument 'mat' is of invalid type: {t}".format(t=type(mat)))

    elif not np.shape(mat) == (3,3):
        raise ValueError("Argument 'mat' must have dimensions '(3,3)', not {d}".format(d=np.shape(mat)))

    elif not isinstance(deg, (int,float)):
        raise TypeError("Argument 'deg' must be of types 'int' or 'float', not {t}".format(t=type(deg)))

    theta = deg* math.pi / 180

    rotation = np.array(
        [1.0,0.0,0.0,
        0.0, math.cos(theta), -math.sin(theta),
        0.0, math.sin(theta), math.cos(theta)]
    ).reshape(3,3)

    return np.matmul(mat, rotation)


def rotateY(mat, deg):

    # Type Checking
    if not isinstance(mat, (list, np.ndarray)):
        raise TypeError("Argument 'mat' is of invalid type: {t}".format(t=type(mat)))

    elif not np.shape(mat) == (3,3):
        raise ValueError("Argument 'mat' must have dimensions '(3,3)', not {d}".format(d=np.shape(mat)))

    elif not isinstance(deg, (int,float)):
        raise TypeError("Argument 'deg' must be of types 'int' or 'float', not {t}".format(t=type(deg)))

    theta = deg* math.pi / 180

    rotation = np.array(
        [math.cos(theta), 0.0, math.sin(theta),
        0.0, 1.0, 0.0,
        -math.sin(theta), 0, math.cos(theta)]
    ).reshape(3,3)

    return np.matmul(mat, rotation)


def rotateZ(mat, deg):

    # Type Checking
    if not isinstance(mat, (list, np.ndarray)):
        raise TypeError("Argument 'mat' is of invalid type: {t}".format(t=type(mat)))

    elif not np.shape(mat) == (3,3):
        raise ValueError("Argument 'mat' must have dimensions '(3,3)', not {d}".format(d=np.shape(mat)))

    elif not isinstance(deg, (int,float)):
        raise TypeError("Argument 'deg' must be of types 'int' or 'float', not {t}".format(t=type(deg)))

    theta = deg* math.pi / 180

    rotation = np.array(
        [math.cos(theta), -math.sin(theta), 0.0,
        math.sin(theta), math.cos(theta), 0.0,
        0.0, 0.0, 1.0]
    ).reshape(3,3)

    return np.matmul(mat, rotation)