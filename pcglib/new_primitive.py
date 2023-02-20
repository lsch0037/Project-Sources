import numpy as np

from vec3 import vec3
from mat4 import mat4

class new_primitive():
    # Constructor with 2 optional arguments: (postition:vec3, rotation:mat4)
    def __init__(self, pos, rot):
        self.pos = pos
        self.rot = rot

    def set(self, material, buffer):
        pass

class new_cube(new_primitive):
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
                    # print(current_pos)

                    buffer.set(current_pos, material)