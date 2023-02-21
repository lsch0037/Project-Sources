from Compound import Compound

from vec3 import vec3
from mat4 import mat4

class primitive(Compound):
    # Constructor with 2 optional arguments: (postition:vec3, rotation:mat4)
    def __init__(self, pos, rot):
        # super().__init__()
        self.children = []
        self.pos = pos
        self.rot = rot

    def set(self, material, buffer):
        pass

class cube(primitive):
    def __init__(self, pos, rot, size):
        super().__init__(pos, rot)
        self.size = size

    def set(self, material, buffer):
        current_pos = vec3()

        x_d = vec3(self.rot[0][0:3])
        y_d = vec3(self.rot[1][0:3])
        z_d = vec3(self.rot[2][0:3])

        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    current_pos = self.pos + x_d*i + y_d*j + z_d*k

                    buffer.set(current_pos, material)

class cuboid(primitive):
    # Constructor for a cuboid primitive
    # dim: a vector where the magnitude of i,j and k determine the dimensions of the cuboid in each direction
    def __init__(self, pos, rot, dim):
        super().__init__(pos, rot)
        self.dim = dim

    def set(self, material, buffer):
        current_pos = vec3()

        x_d = vec3(self.rot[0][0:3])
        y_d = vec3(self.rot[1][0:3])
        z_d = vec3(self.rot[2][0:3])

        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                for k in range(self.dim[2]):
                    current_pos = self.pos + x_d*i + y_d*j + z_d*k

                    buffer.set(current_pos, material)

class sphere(primitive):
    def __init__(self, pos, rot, rad):
        super().__init__(pos, rot)
        self.rad = rad

    def set(self, material, buffer):
        pos0 = self.pos - [self.rad, self.rad, self.rad]

        for x in range(0,2*self.rad):
            for y in range(0,2*self.rad):
                for z in range(0,2*self.rad):
                    current_pos = pos0 + [x,y,z]

                    d = self.pos - current_pos
                    if(abs(d) <= self.rad):
                        buffer.set(current_pos, material)

class cylinder(primitive):
    def __init__(self, pos, rot, rad, len):
        super().__init__(pos, rot)
        self.rad = rad
        self.len = len

    def set(self, material, buffer):
        # TODO SET CYLINDER
        pass