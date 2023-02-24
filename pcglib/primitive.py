from pcglib.compound import compound

from pcglib.vec3 import vec3
from pcglib.mat4 import mat4

class primitive(compound):
    # Constructor with 2 optional arguments: (postition:vec3, rotation:mat4)
    def __init__(self, pos, rot, material):
        # super().__init__()
        self.children = []
        self.pos = pos
        self.rot = rot
        self.material = material


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
        super().__init__(pos, rot,material)
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
    def __init__(self, pos, rot, material, rad):
        super().__init__(pos, rot,material)
        self.rad = rad

    def set(self, buffer):
        pos0 = self.pos - [self.rad, self.rad, self.rad]

        for x in range(0,2*self.rad):
            for y in range(0,2*self.rad):
                for z in range(0,2*self.rad):
                    current_pos = pos0 + [x,y,z]

                    d = self.pos - current_pos
                    if(abs(d) <= self.rad):
                        buffer.set(current_pos, self.material)

class cylinder(primitive):
    def __init__(self, pos, rot, material, rad, len):
        super().__init__(pos, rot,material)
        self.rad = rad
        self.len = len

    def set(self, buffer):
        # TODO SET CYLINDER
        pass