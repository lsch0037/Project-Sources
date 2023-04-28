from csglib.compound import compound
from csglib.buffer import *

import numpy as np

class primitive(compound):
    def __init__(self, material):
        self.children = []
        self.material = material

    def _set_internal(self, operator):
        raise ValueError("Cannot call _set_internal on generic primitive")

    def set(self, pos, rot):
        return self._set_internal(pos,rot,"set")

    def unset(self, pos, rot):
        return self._set_internal(pos,rot,"unset")


class cube(primitive):
    def __init__(self, material, size):
        super().__init__(material)
        self.size = size

    def _set_internal(self, pos, rot, op):
        buf = buffer()

        x_d = np.dot(rot, np.array([1,0,0]))
        y_d = np.dot(rot, np.array([0,1,0]))
        z_d = np.dot(rot, np.array([0,0,1]))

        for i in range(self.size*2):
            for j in range(self.size*2):
                for k in range(self.size*2):
                    current_pos = pos + x_d*(i/2) + y_d*(j/2) + z_d*(k/2)

                    if op == "set":
                        buf.set(current_pos, self.material.get(current_pos))

                    elif op == "unset":
                        buf.unset(current_pos)
        
        return buf

    # Get bounds of Cube Primitive
    def getBounds(self):
        min = np.array([0,0,0])
        max = np.array([self.size, self.size, self.size])
        
        return min, max

    def __repr__(self):
        return 'Cube'

class cuboid(primitive):
    # Constructor for a cuboid primitive
    # dim: a vector where the magnitude of i,j and k determine the dimensions of the cuboid in each direction
    def __init__(self, material, dim):
        super().__init__(material)
        self.dim = dim

    # def _set_internal(self, op):
    def _set_internal(self, pos, rot, op):
        buf = buffer()

        x_d = np.dot(rot, np.array([1,0,0]))
        y_d = np.dot(rot, np.array([0,1,0]))
        z_d = np.dot(rot, np.array([0,0,1]))

        for i in range(int(self.dim[0])*2):
            for j in range(int(self.dim[1])*2):
                for k in range(int(self.dim[2])*2):
                    current_pos = pos + x_d*(i/2) + y_d*(j/2) + z_d*(k/2)

                    if op == "set":
                        buf.set(current_pos, self.material.get(current_pos))
                    elif op == "unset":
                        buf.unset(current_pos)

        return buf

    # Get bounds of Cube Primitive
    def getBounds(self):
        min = np.array([0,0,0])
        max = self.dim
        
        return min, max

    def __repr__(self):
        return 'Cuboid'

class sphere(primitive):
    def __init__(self, material, rad):
        super().__init__(material)
        self.rad = rad

    def _set_internal(self,pos,rot, op):
        buf = buffer()

        pos0 = pos - np.array([self.rad, self.rad, self.rad])

        for x in range(int(2*self.rad)):
            for y in range(int(2*self.rad)):
                for z in range(int(2*self.rad)):
                    current_pos = pos0 + np.array([x,y,z])
                    dist = np.linalg.norm(pos - current_pos)  

                    if dist <= self.rad:
                        if op == "set":
                            buf.set(current_pos, self.material.get(current_pos))
                        elif op == "unset":
                            buf.unset(current_pos)
        
        return buf

    def getBounds(self):
        min = np.array([-self.rad, -self.rad, -self.rad])
        max = np.array([self.rad, self.rad, self.rad])

        return min, max

    def __repr__(self):
        return 'Sphere'

class cylinder(primitive):
    def __init__(self, material, rad, len):
        super().__init__(material)
        self.rad = rad
        self.len = len

    def _set_internal(self, pos, rot, op):
        buf = buffer()

        x_d = np.dot(rot, np.array([1,0,0]))
        y_d = np.dot(rot, np.array([0,1,0]))
        z_d = np.dot(rot, np.array([0,0,1]))

        for h in range(self.len*2):
            center_pos = pos + y_d*(h/2)
            for i in range(-self.rad*2, self.rad*2):
                for j in range(-self.rad*2, self.rad*2):
                    current_pos = pos + x_d*(i/2) + y_d*(h/2) + z_d*(j/2)
                    dist = np.linalg.norm(current_pos - center_pos)  

                    if dist <= self.rad:
                        if op == "set":
                            buf.set(current_pos, self.material.get(current_pos))
                        elif op == "unset":
                            buf.unset(current_pos)
        
        return buf

    def getBounds(self):
        min = np.array(-self.rad, 0, -self.rad)
        max = np.array(self.rad, self.len, self.rad)

        return min, max

    def __repr__(self):
        return 'Cylinder'
        

class pyramid(primitive):
    pass

class prism(primitive):
    pass

class cone(primitive):
    pass