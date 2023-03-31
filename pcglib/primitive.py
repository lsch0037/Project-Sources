from pcglib.compound import compound
from pcglib.boundingBox import *
from pcglib.buffer import *

import numpy as np

class primitive(compound):
    def __init__(self, pos, rot, material):
        self.children = []
        self.pos = pos
        self.rot = rot
        self.material = material

    def _set_internal(self, operator):
        raise ValueError("Cannot call _set_internal on generic primitive")

    def set(self):
        return self._set_internal("set")

    def unset(self):
        return self._set_internal("unset")


class cube(primitive):
    def __init__(self, pos, rot,material, size):
        super().__init__(pos, rot, material)
        self.size = size

    def _set_internal(self, op):
        buf = buffer()

        x_d = np.dot(self.rot,np.array([1,0,0]))
        y_d = np.dot(self.rot,np.array([0,1,0]))
        z_d = np.dot(self.rot,np.array([0,0,1]))

        for i in range(self.size*2):
            for j in range(self.size*2):
                for k in range(self.size*2):
                    current_pos = self.pos + x_d*(i/2) + y_d*(j/2) + z_d*(k/2)

                    if op == "set":
                        buf.set(current_pos, self.material.get(current_pos))

                    elif op == "unset":
                        buf.unset(current_pos)
        
        return buf

class cuboid(primitive):
    # Constructor for a cuboid primitive
    # dim: a vector where the magnitude of i,j and k determine the dimensions of the cuboid in each direction
    def __init__(self, pos, rot, material, dim):
        super().__init__(pos, rot, material)
        self.dim = dim

    def _set_internal(self, op):
        buf = buffer()

        x_d = np.dot(self.rot,np.array([1,0,0]))
        y_d = np.dot(self.rot,np.array([0,1,0]))
        z_d = np.dot(self.rot,np.array([0,0,1]))

        for i in range(int(self.dim[0])*2):
            for j in range(int(self.dim[1])*2):
                for k in range(int(self.dim[2])*2):
                    current_pos = self.pos + x_d*(i/2) + y_d*(j/2) + z_d*(k/2)

                    if op == "set":
                        buf.set(current_pos, self.material.get(current_pos))
                    elif op == "unset":
                        buf.unset(current_pos)

        return buf

class sphere(primitive):
    def __init__(self, pos, material, rad):
        super().__init__(pos, np.identity(3), material)
        self.rad = rad

    def _set_internal(self, op):
        buf = buffer()
        print("Pos:{p}, Rad:{r}".format(p=self.pos, r=self.rad))

        pos0 = self.pos - np.array([self.rad, self.rad, self.rad])

        for x in range(0,2*self.rad):
            for y in range(0,2*self.rad):
                for z in range(0,2*self.rad):
                    current_pos = pos0 + np.array([x,y,z])
                    dist = np.linalg.norm(self.pos - current_pos)  

                    if dist <= self.rad:
                        if op == "set":
                            # buffer.set(current_pos, self.material)
                            buf.set(current_pos, self.material.get(current_pos))
                        elif op == "unset":
                            buf.unset(current_pos)
        
        return buf

    # !Rotating a sphere does nothing
    def rotateX(self, theta):
        return
    
    def rotateY(self, theta):
        return

    def rotateZ(self, theta):
        return


class cylinder(primitive):
    def __init__(self, pos, rot, material, rad, len):
        super().__init__(pos, rot,material)
        self.rad = rad
        self.len = len

    def _set_internal(self, op):
        buf = buffer()

        x_d = np.dot(self.rot,np.array([1,0,0]))
        y_d = np.dot(self.rot,np.array([0,1,0]))
        z_d = np.dot(self.rot,np.array([0,0,1]))

        for h in range(self.len*2):
            center_pos = self.pos + y_d*(h/2)
            for i in range(-self.rad*2, self.rad*2):
                for j in range(-self.rad*2, self.rad*2):
                    current_pos = self.pos + x_d*(i/2) + y_d*(h/2) + z_d*(j/2)
                    dist = np.linalg.norm(current_pos - center_pos)  

                    if dist <= self.rad:
                        if op == "set":
                            buf.set(current_pos, self.material.get(current_pos))
                        elif op == "unset":
                            buf.unset(current_pos)
        
        return buf