import numpy as np

import ServerOperations
from GlobalVariables import mc
from Compound import Compound
from VectorOperations import Vector
from Buffer import Buffer

class Primitive(Compound):

    def __init__(self, O, material, replacing=-1):
        self.children = []
        self.O = O
        self.material = material
        self.replacing = replacing


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


class Sphere(Primitive):
    def __init__(self, O, radius, material):
        super().__init__(O, material)
        self.radius = radius

    def set(self, buffer):
        self._set(self.material, buffer)

    def _set(self,material, buffer):
        pos0 = self.O - [self.radius, self.radius, self.radius]

        for x in range(0,2*self.radius):
            for y in range(0,2*self.radius):
                for z in range(0,2*self.radius):
                    current_pos = pos0 + [x,y,z]

                    d = self.O - current_pos
                    if(d.getLength() <= self.radius):
                        buffer.set(current_pos[0], current_pos[1], current_pos[2], material)
    

class Cylinder(Primitive):
    #define a cylinder with starting from O and in direction and length defined by V, of given radius
    def __init__(self, O, V, radius):
        super().__init__(O)
        self.V = V
        self.radius = radius
    
    #sets the cylinder out of given material in the game world
    def set(self, material):
        # TODO IMPLEMENT
        pass
