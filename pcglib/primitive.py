from pcglib.compound import compound

from pcglib.vec3 import vec3
from pcglib.mat4 import mat4

import numpy as np

class primitive(compound):
    # Constructor with 2 optional arguments: (postition:vec3, rotation:mat4)
    def __init__(self, pos, rot, material):
        # super().__init__()
        self.children = []
        self.pos = pos
        self.rot = rot
        self.material = material

    # ? UNSET FUNCTION TO SIMPLIFY DIFFERENCE (CARVING)


class cube(primitive):
    def __init__(self, pos, rot,material, size):
        super().__init__(pos, rot, material)
        self.size = size

    def set(self, buffer):
        current_pos = vec3()

        x_d = vec3(self.rot[0][0:3])
        y_d = vec3(self.rot[1][0:3])
        z_d = vec3(self.rot[2][0:3])

        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    current_pos = self.pos + x_d*i + y_d*j + z_d*k

                    buffer.set(current_pos, self.material)

class cuboid(primitive):
    # Constructor for a cuboid primitive
    # dim: a vector where the magnitude of i,j and k determine the dimensions of the cuboid in each direction
    def __init__(self, pos, rot, material, dim):
        super().__init__(pos, rot, material)
        self.dim = dim

    def set(self, buffer):
        current_pos = vec3()

        x_d = vec3(self.rot[0][0:3])
        y_d = vec3(self.rot[1][0:3])
        z_d = vec3(self.rot[2][0:3])

        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                for k in range(self.dim[2]):
                    current_pos = self.pos + x_d*i + y_d*j + z_d*k

                    buffer.set(current_pos, self.material)

class sphere(primitive):
    def __init__(self, pos, material, rad):
        # TODO: HARDCODE ROTATION AS IDENTITY
        rot = mat4()
        rot.identity()
        super().__init__(pos, rot,material)
        self.rad = rad

    def set(self, buffer):
        pos0 = np.array(self.pos) - np.array([self.rad, self.rad, self.rad])

        for x in range(0,2*self.rad):
            for y in range(0,2*self.rad):
                for z in range(0,2*self.rad):
                    current_pos = pos0 + np.array([x,y,z])

                    if np.linalg.norm(self.pos - current_pos) <= self.rad:
                        buffer.set(current_pos, self.material)

class cylinder(primitive):
    def __init__(self, pos, rot, material, rad, len):
        super().__init__(pos, rot,material)
        self.rad = rad
        self.len = len

    def set(self, buffer):
        print("Setting cylinder")

        x_d = np.array(self.rot[0][0:3])
        y_d = np.array(self.rot[1][0:3])
        z_d = np.array(self.rot[2][0:3])


        for h in range(self.len):
            center_pos = self.pos + y_d*h
            for i in range(-self.rad, self.rad):
                for j in range(-self.rad, self.rad):
                    current_pos = self.pos + x_d*i + y_d*h + z_d*j

                    if np.linalg.norm(current_pos - center_pos) <= self.rad:
                        buffer.set(current_pos, self.material)
