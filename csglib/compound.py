from csglib.buffer import buffer

import numpy as np
import math

class compound():
    def __init__(self,children = []):
        self.children = children

    def addChild(self,child):
        self.children.append(child)

    def getChild(self, index):
        return self.children[index]


    # https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python
    def __str__(self, level=0):
        ret = "\t"*level+repr(self)+"\n"
        for child in self.children:
            print(type(child))
            if child == None:
                return "None"
            else:
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return 'Generic Node'


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

    def shiftBy(self,other, offset):
        return shiftNode(offset, [self,other])

    def set(self,pos,rot, buf):
        raise ValueError("Cannot call 'set' on generic node")

    def unset(self,pos,rot,buf):
        raise ValueError("Cannot call 'unset' on generic node")


class unionNode(compound):
    def set(self,pos,rot):
        print("Evaluating {}".format("union"))
        newBuf = buffer()

        for child in self.children:
            buf = child.set(pos,rot)
            buf.write(newBuf)

        return newBuf

    def unset(self,pos,rot):
        print("Evaluating {}".format("union"))
        newBuf = buffer()

        for child in self.children:
            buf = child.unset(pos, rot)
            buf.write(newBuf)

        return newBuf

    def __repr__(self):
        return 'Union Node'


class differenceNode(compound):
    def set(self,pos,rot):
        print("Evaluating {}".format("difference"))
        newBuf = buffer()

        buf1 = self.children[0].set(pos,rot)
        buf1.write(newBuf)

        for i in range(1,len(self.children)):
            buf2 = self.children[i].set(pos,rot)
            buf2.unwrite(newBuf)

        return newBuf

    
    def unset(self,pos,rot):
        print("Evaluating {}".format("difference"))
        newBuf = buffer()

        buf1 = self.children[0].set(pos,rot)
        buf1.unwrite(newBuf)

        for i in range(1,len(self.children)):
            buf2 = self.children[i].set(pos,rot)
            buf2.write(newBuf)

        return newBuf

    def __repr__(self):
        return 'Difference Node'

class intersectionNode(compound):
    def set(self,pos,rot):
        print("Evaluating {}".format("intersection"))
        # newBuf = buffer()

        interBuf = self.children[0].set(pos, rot) 

        for i in range(1, len(self.children)):
            child = self.children[i]

            buf = child.set(pos,rot)
            interBuf = buf.intersection(interBuf)

        return interBuf

    def __repr__(self):
        return 'Intersection Node'

class onGroundNode(compound):
    def __init__(self,game, children=[]):
        super().__init__(children)
        self.game = game

    def set(self, pos,rot):
        print("Evaluating {}".format("On Ground"))
        groundHeight = self.game.getHeight(pos[0],pos[2])
        new_pos = np.array([pos[0], groundHeight + 1, pos[2]])

        child_buf = self.children[0].set(pos, rot)

        bottom = child_buf.getBottom()

        offset = new_pos - bottom

        child_buf.shift(offset)

        return child_buf

    def __repr__(self):
        return 'On Ground Node'

class prepositionNode(compound):
    def __init__(self, f1, f2, children=[]):
        super().__init__(children)
        self.f1 = f1
        self.f2 = f2

    def set(self,pos,rot):
        print("Evaluating {}".format("Preposition"))
        print("Pos:{p}, Rot:{r}".format(p=pos,r=rot))

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

    def unset(self, pos, rot):
        pass

    def __repr__(self):
        return 'Preposition Node'


class shiftNode(compound):
    def __init__(self,offset, children=[]):
        super().__init__(children)
        self.offset = offset

    def set(self,pos,rot):
        print("Evaluating {}".format("Shift Node"))
        print("Pos:{p}, Rot:{r}".format(p=type(pos),r=type(rot)))

        offset_rot = np.dot(rot, self.offset)
        print("Offset Rotated:{}".format(offset_rot))

        new_pos = np.add(pos , offset_rot)
        print("New pos:{}".format(new_pos))

        return self.children[0].set(new_pos, rot)

    def unset(self,pos,rot):
        print("Evaluating {}".format("Shift Node"))
        new_pos = np.add(pos , np.dot(rot, self.offset))

        return self.children[0].unset(new_pos, rot)

    def __repr__(self):
        return 'Shift Node'

class onNode(compound):
    def set(self, pos, rot):
        buf = buffer()

        bufA = self.children[0].set(pos, rot)
        bufB = self.children[1].set(pos, rot)

        return buf

# class northNode(compound):
#     def set(self, pos, rot):

#         buf = buffer()

#         # ! Set obj1 at pos
#         buf1 = self.children[0].set(pos, rot)

#         # ! Pos2 is the center of the obj1 bounding box
#         north = buf1.getNorth()

#         # ! Set obj2 at pos2
#         temp_buf = self.children[1].set(pos, rot)
#         south = temp_buf.getSouth()

#         difference = north - south + 0.5

#         # buf2 = self.children[1].set(pos + difference, rot)
#         temp_buf.shift(difference)

#         buf1.write(buf)
#         temp_buf.write(buf)

#         return buf

#     def __repr__(self):
#         return 'North Node'

class rotationNode(compound):
    def __init__(self,axis, deg, children=[]):
        super().__init__(children)

        functions = [rotateX, rotateY, rotateZ]

        self.f = functions[axis]
        self.deg = deg


    def set(self,pos,prev_rot):
        print("Evaluating {}".format("Rotation"))

        newBuf = buffer()

        new_rot = self.f(prev_rot, self.deg)

        for child in self.children:
            buf = child.set(pos, new_rot)
            buf.write(newBuf)

        return newBuf


    def unset(self,pos, prev_rot):
        print("Evaluating {}".format("Rotation"))
        newBuf = buffer()

        new_rot = self.f(prev_rot, self.deg)

        for child in self.children:
            buf = child.set(pos, new_rot)
            buf.unwrite(newBuf)

        return newBuf

    def __repr__(self):
        return 'Rotation Node'

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