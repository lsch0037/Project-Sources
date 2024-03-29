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

    # Function to recursively print the tree structure
    # code inspired by: https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python
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
        return 'End'


    # !Bounding Box
    def getBounds(self):
        min = np.array([0,0,0])
        max = np.array([0,0,0])

        return min, max

    def getTop(self):
        min,max = self.getBounds()
        mid = (min + max)/2

        return np.array([mid[0], max[1], mid[2]])

    def getBottom(self):
        min,max = self.getBounds()
        mid = (min + max)/2

        return np.array([mid[0], min[1], mid[2]])

    def getCenter(self):
        min,max = self.getBounds()
        mid = (min + max)/2

        return mid

    def getEast(self):
        min,max = self.getBounds()
        mid = (min + max)/2

        return np.array([max[0],mid[1],mid[2]])

    def getSouth(self):
        min,max = self.getBounds()
        mid = (min + max)/2

        return np.array([mid[0],mid[1],max[2]])

    def getWest(self):
        min,max = self.getBounds()
        mid = (min + max)/2

        return np.array([min[0],mid[1],mid[2]])

    def getNorth(self):
        min,max = self.getBounds()
        mid = (min + max)/2

        return np.array([mid[0],mid[1],min[2]])

    # !Geometric Operations
    # Adds addition node as parent and node as sibling
    def union(self, other):
        return unionNode([self,other])

    # Adds subtraction node as parent and node as sibling
    def difference(self, other):
        return differenceNode([self,other])

    def intersection(self, other):
        return intersectionNode([self,other])


    # !Preposition Operations
    # def onTopOf(self,other):
    #     return prepositionNode(compound.getBottom,compound.getTop, [self,other])

    # def under(self,other):
    #     return prepositionNode(compound.getTop, compound.getBottom, [self,other])

    # def insideOf(self,other):
    #     return prepositionNode(compound.getCenter, compound.getCenter, [self,other])

    # def eastOf(self,other):
    #     return prepositionNode(compound.getWest, compound.getEast, [self,other])

    # def southOf(self,other):
    #     return prepositionNode(compound.getNorth,compound.getSouth, [self,other])

    # def westOf(self,other):
    #     return prepositionNode(compound.getEast, compound.getWest, [self,other])

    # def northOf(self,other):
    #     return prepositionNode(compound.getSouth, compound.getNorth, [self,other])

    def shiftBy(self,other, offset):
        return shiftNode(offset, [self,other])

    def set(self,pos,rot):
        return buffer()



class unionNode(compound):
    def set(self,pos,rot):
        print("Evaluating {}".format("union"))
        buf = buffer()

        for child in self.children:
            temp_buf = child.set(pos,rot)
            temp_buf.write(buf)

        return buf


    def getBounds(self):
        min = np.array([np.inf, np.inf, np.inf])
        max = np.array([-np.inf, -np.inf, -np.inf])

        for child in self.children:
            child_min, child_max = child.getBounds()

            for dim in range(3):
                if child_max[dim] > max[dim]:
                    max[dim] = child_max[dim]


                if child_min[dim] < min[dim]:
                    min[dim] = child_min[dim]

        return min, max

    def __repr__(self):
        return 'Union'


class differenceNode(compound):
    def set(self,pos,rot):
        print("Evaluating {}".format("difference"))

        buf = self.children[0].set(pos,rot)

        for i in range(1,len(self.children)):
            other_buf = self.children[i].set(pos, rot)
            other_buf.unwrite(buf)
        
        return buf
    
    def getBounds(self):
        return self.children[0].getBounds()

    def __repr__(self):
        return 'Difference'


class intersectionNode(compound):
    def set(self,pos,rot):
        print("Evaluating {}".format("intersection"))

        interBuf = self.children[0].set(pos, rot) 

        for i in range(1, len(self.children)):

            buf = self.children[i].set(pos,rot)
            interBuf = buf.intersection(interBuf)

        return interBuf

    def getBounds(self):
        min, max = self.children[0].getBounds()
        
        for child in self.children:
            child_max, child_min = child.getBounds()

            for dim in range(3):
                if child_max[dim] < max[dim]:
                    max = child_max[dim]

                if child_min[dim] > min[dim]:
                    min = child_min[dim]

        return min, max

    def __repr__(self):
        return 'Intersection'

class prepositionNode(compound):
    def __init__(self, prep, children=[]):
        super().__init__(children)
        self.prep = prep

    def getDifference(self):
        if self.prep == "North":
            anchor1 = self.children[0].getSouth()
            anchor2 = self.children[1].getNorth()

            return np.array([0, 0, anchor2[2] - anchor1[2]])

        elif self.prep == "South":
            anchor1 = self.children[0].getNorth()
            anchor2 = self.children[1].getSouth()

            return np.array([0, 0, anchor2[2] - anchor1[2]])

        elif self.prep == "East":
            anchor1 = self.children[0].getWest()
            anchor2 = self.children[1].getEast()

            return np.array([anchor2[0] - anchor1[0], 0, 0])

        elif self.prep == "West":
            anchor1 = self.children[0].getEast()
            anchor2 = self.children[1].getWest()

            return np.array([anchor2[0] - anchor1[0], 0, 0])

        elif self.prep == "On":
            anchor1 = self.children[0].getBottom()
            anchor2 = self.children[1].getTop()

            return np.array([0, anchor2[1] - anchor1[1], 0])

        elif self.prep == "Under":
            anchor1 = self.children[0].getTop()
            anchor2 = self.children[1].getBottom()

            return np.array([0, anchor2[1] - anchor1[1], 0])


    def set(self,pos,rot):
        buf = buffer()

        diff = self.getDifference()

        print(pos+diff)

        buf1 = self.children[0].set(pos + diff, rot)
        buf2 = self.children[1].set(pos, rot)

        buf1.write(buf)
        buf2.write(buf)

        return buf

    def getBounds(self):
        diff = self.getDifference()

        min1,max1 = self.children[0].getBounds()
        min2,max2 = self.children[1].getBounds()

        # Shift first node by offset
        min1shifted = min1 + diff
        max1shifted = max1 + diff

        # Calculate min and max
        min = np.array([0,0,0])
        max = np.array([0,0,0])

        for dim in range(3):
            if min1shifted[dim] < min2[dim]:
                min[dim] = min1shifted[dim]
            else:
                min[dim] = min2[dim]

            if max1shifted[dim] > max2[dim]:
                max[dim] = max1shifted[dim]
            else:
                max[dim] = max2[dim]

        return min, max

    def __repr__(self):
        return self.prep


class onGroundNode(compound):
    def __init__(self,game, children=[]):
        super().__init__(children)
        self.game = game


    def set(self, pos, rot):
        print("Evaluating {}".format("On Ground"))
        groundHeight = self.game.getHeight(pos[0],pos[2])

        bottom = self.children[0].getBottom()

        diff = groundHeight - (pos[1] + bottom[1]) + 1

        newPos = pos
        newPos[1] += diff
        
        return self.children[0].set(newPos, rot)


    def getBounds(self):
        return self.children[0].getBounds() 

    def __repr__(self):
        return 'On Ground'


class shiftNode(compound):
    def __init__(self,offset, children=[]):
        super().__init__(children)
        self.offset = offset

    def set(self,pos,rot):
        print("Evaluating {}".format("Shift Node"))


        offset_rot = np.dot(rot, self.offset)

        print("Pos:{}, Offset:{}".format(pos, offset_rot))
        new_pos = np.add(pos , offset_rot)

        buf = buffer()

        for child in self.children:
            other_buf = child.set(new_pos, rot)
            other_buf.write(buf)

        return buf

    def getBounds(self):
        _min, _max = self.children[0].getBounds()

        # Shifting the bounds by the offset
        min = _min + self.offset
        max = _max + self.offset

        return min, max

    def __repr__(self):
        return 'Shift'


class rotationNode(compound):
    def __init__(self,axis, deg, children=[]):
        super().__init__(children)

        self.axis = axis
        self.deg = deg


    def set(self,pos,prev_rot):
        print("Evaluating {}".format("Rotation"))

        buf = buffer()

        new_rot = rotate(prev_rot, self.axis, self.deg)

        for child in self.children:
            other_buf = child.set(pos, new_rot)
            other_buf.write(buf)

        return buf

    # Returns the bounds relative to the implicit origin position of the algorithm (at neutral rotation)
    def getBounds(self):
        child_min, child_max = self.children[0].getBounds()

        # Find the actual vertices of the bounding box
        vertices = []
        vertices.append(child_min)
        vertices.append(np.array([child_min[0], child_min[1], child_max[2]]))
        vertices.append(np.array([child_min[0], child_max[1], child_min[2]]))
        vertices.append(np.array([child_max[0], child_min[1], child_min[2]]))
        vertices.append(np.array([child_min[0], child_max[1], child_max[2]]))
        vertices.append(np.array([child_max[0], child_min[1], child_max[2]]))
        vertices.append(np.array([child_max[0], child_max[1], child_min[2]]))
        vertices.append(child_max)

        id = np.identity(3)
        rot = rotate(id, self.axis, self.deg)


        rot_vertices = []

        # Rotate all vertices
        for vert in vertices:
            rot_vertices.append(np.matmul(rot, vert))

        # Find new min and max in each direction
        max = np.array([-np.inf, -np.inf, -np.inf])
        min = np.array([np.inf, np.inf, np.inf])

        for vert in rot_vertices:
            for dim in range(3):
                if vert[dim] < min[dim]:
                    min[dim] = vert[dim]

                elif vert[dim] > max[dim]:
                    max[dim] = vert[dim]

        return min, max

    def __repr__(self):
        return 'Rotation'

def rotate(mat, axis, deg):
    # Type Checking
    if not isinstance(mat, (list, np.ndarray)):
        raise TypeError("Argument 'mat' is of invalid type: {t}".format(t=type(mat)))

    elif not np.shape(mat) == (3,3):
        raise ValueError("Argument 'mat' must have dimensions '(3,3)', not {d}".format(d=np.shape(mat)))

    elif not isinstance(deg, (int,float)):
        raise TypeError("Argument 'deg' must be of types 'int' or 'float', not {t}".format(t=type(deg)))

    theta = deg* math.pi / 180

    rotation = None

    if axis == 0:
        rotation = np.array(
            [1.0,0.0,0.0,
            0.0, math.cos(theta), -math.sin(theta),
            0.0, math.sin(theta), math.cos(theta)]
        ).reshape(3,3)

    elif axis == 1:
        rotation = np.array(
            [math.cos(theta), 0.0, math.sin(theta),
            0.0, 1.0, 0.0,
            -math.sin(theta), 0, math.cos(theta)]
        ).reshape(3,3)

    elif axis == 2:
        rotation = np.array(
            [math.cos(theta), -math.sin(theta), 0.0,
            math.sin(theta), math.cos(theta), 0.0,
            0.0, 0.0, 1.0]
        ).reshape(3,3)

    else:
        raise ValueError("Invalid axis: {}".format(axis))

    return np.matmul(mat, rotation)