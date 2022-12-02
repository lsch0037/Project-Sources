import numpy as np

import ServerOperations
from GlobalVariables import mc
from Compound import Compound

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

    def set(self):
        self._set(self.material)

    def carve(self):
        self._set(0)

    def _set(self, material):

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
                    ServerOperations.set_block(current_pos, material, self.replacing)


class Sphere(Primitive):
    def __init__(self, O, radius):
        super().__init__(O)
        self.radius = radius

    #Returns the position vector that is a normal on the surface of the sphere pointing in the direction vector
    def normal(direction):
        return []
    
    def set(self,material):
        pos1 = np.subtract(self.O, [self.radius, self.radius, self.radius])

        for x in range(0,2*self.radius):
            for y in range(0,2*self.radius):
                for z in range(0,2*self.radius):
                    current_pos = pos1 + [x,y,z]

                    if(get_length(self.O - current_pos) <= self.radius):
                        ServerOperations.set_block(current_pos, material)
    

class Cylinder(Primitive):
    #define a cylinder with starting from O and in direction and length defined by V, of given radius
    def __init__(self, O, V, radius):
        super().__init__(O)
        self.V = V
        self.radius = radius
    
    #sets the cylinder out of given material in the game world
    def set(self, material):
        print("TO BE IMPLEMENTED")

