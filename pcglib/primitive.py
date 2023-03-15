from pcglib.compound import compound

import numpy as np
import math

class primitive(compound):
    def __init__(self, pos, rot, material):
        self.children = []
        self.pos = pos
        self.rot = rot
        self.material = material

    def _set_internal(self, buf, operator):
        raise ValueError("Cannot call _set_internal on generic primitive")

    def set(self, buf):
        self._set_internal(buf, "set")

    def unset(self, buf):
        self._set_internal(buf, "unset")

    # def rotateX(self, deg):
    #     theta = deg* math.pi / 180

    #     rotation = np.array(
    #         [1.0,0.0,0.0,
    #         0.0, math.cos(theta), -math.sin(theta),
    #         0.0, math.sin(theta), math.cos(theta)]
    #     ).reshape(3,3)

    #     self.rot = np.matmul(self.rot, rotation)

    # def rotateY(self, deg):
    #     theta = deg* math.pi / 180

    #     rotation = np.array(
    #         [math.cos(theta), 0.0, math.sin(theta),
    #         0.0, 1.0, 0.0,
    #         -math.sin(theta), 0, math.cos(theta)]
    #     ).reshape(3,3)

    #     self.rot = np.matmul(self.rot, rotation)

    # def rotateZ(self, deg):
    #     theta = deg* math.pi / 180

    #     rotation = np.array(
    #         [math.cos(theta), -math.sin(theta), 0.0,
    #         math.sin(theta), math.cos(theta), 0.0,
    #         0.0, 0.0, 1.0]
    #     ).reshape(3,3)

    #     self.rot = np.matmul(self.rot, rotation)


class cube(primitive):
    def __init__(self, pos, rot,material, size):
        super().__init__(pos, rot, material)
        self.size = size

    def _set_internal(self,buffer, op):
        x_d = self.rot[0]
        y_d = self.rot[1]
        z_d = self.rot[2]

        for i in range(self.size*2):
            for j in range(self.size*2):
                for k in range(self.size*2):
                    current_pos = self.pos + x_d*(i/2) + y_d*(j/2) + z_d*(k/2)

                    if op == "set":
                        buffer.set(current_pos, self.material)
                    elif op == "unset":
                        buffer.unset(current_pos)

class cuboid(primitive):
    # Constructor for a cuboid primitive
    # dim: a vector where the magnitude of i,j and k determine the dimensions of the cuboid in each direction
    def __init__(self, pos, rot, material, dim):
        super().__init__(pos, rot, material)
        self.dim = dim

    def _set_internal(self, buffer, op):

        x_dir = self.rot[0]
        y_dir = self.rot[1]
        z_dir = self.rot[2]

        for i in range(int(self.dim[0])*2):
            for j in range(int(self.dim[1])*2):
                for k in range(int(self.dim[2])*2):
                    current_pos = self.pos + x_dir*(i/2) + y_dir*(j/2) + z_dir*(k/2)

                    if op == "set":
                        buffer.set(current_pos, self.material)
                    elif op == "unset":
                        buffer.unset(current_pos)


class sphere(primitive):
    def __init__(self, pos, material, rad):
        super().__init__(pos, np.identity(3), material)
        self.rad = rad

    def _set_internal(self, buffer, op):
        pos0 = self.pos - np.array([self.rad, self.rad, self.rad])

        for x in range(0,2*self.rad):
            for y in range(0,2*self.rad):
                for z in range(0,2*self.rad):
                    current_pos = pos0 + np.array([x,y,z])
                    dist = np.linalg.norm(self.pos - current_pos)  

                    if dist <= self.rad:
                        if op == "set":
                            buffer.set(current_pos, self.material)
                        elif op == "unset":
                            buffer.unset(current_pos)

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

    def _set_internal(self, buffer, op):

        x_d = self.rot[0]
        y_d = self.rot[1]
        z_d = self.rot[2]

        for h in range(self.len*2):
            center_pos = self.pos + y_d*(h/2)
            for i in range(-self.rad*2, self.rad*2):
                for j in range(-self.rad*2, self.rad*2):
                    current_pos = self.pos + x_d*(i/2) + y_d*(h/2) + z_d*(j/2)
                    dist = np.linalg.norm(current_pos - center_pos)  

                    if dist <= self.rad:
                        if op == "set":
                            buffer.set(current_pos, self.material)
                        elif op == "unset":
                            buffer.unset(current_pos)

