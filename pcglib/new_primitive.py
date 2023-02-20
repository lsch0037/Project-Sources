import numpy as np

from vec3 import vec3

# class Primitive(Compound):

#     def __init__(self, O, material, replacing=-1):
#         self.children = []
#         self.O = O
#         self.material = material
#         self.replacing = replacing

class new_primitive():
    def __init__(self, pos, rot):
        self._pos = pos
        self._orientation = rot

    # Shift the shape in a certain direction
    def __add__(self, offset):
        if isinstance(offset, vec3):
            self._pos = self._pos + offset
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(offset))

    def __mul__(self, rotation):
        


class Cuboid(Primitive):
    
    def __init__(self, O, X, Y, Z ,material, replacing=-1):
        self.children = []
        self.O = O
        self.material = material
        self.replacing = replacing

        self.X = X
        self.Y = Y
        self.Z = Z

    def set(self, buffer):
        self._set(self.material, buffer)

    def carve(self, buffer):
        self._set(0, buffer)

    def _set(self, material, buffer):

        #If all vectors are orthogonal to each other
        # TODO: MAKE THIS WORK FOR ALL CASES
        prod = self.X * self.Y
        if(prod.getDirection() != self.Z.getDirection()):
            print("Vectors are not orthogonal")
            return

        #Size of the vector in each direction
        len_X = self.X.getLength()
        len_Y = self.Y.getLength()
        len_Z = self.Z.getLength()
        
        dir_X = self.X.getDirection()
        dir_Y = self.Y.getDirection()
        dir_Z = self.Z.getDirection()

        for i in range(0, int(len_X)):
            for j in range(0, int(len_Y)):
                for k in range(0, int(len_Z)):
                    current_pos = self.O + dir_X*i + dir_Y*j + dir_Z*k
                    buffer.set(current_pos[0], current_pos[1], current_pos[2], material)