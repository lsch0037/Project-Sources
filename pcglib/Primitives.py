import numpy as np
from ServerOperations import BasicOperation
from VectorOperations import get_length

class Primitive():

    def __init__(self, O):
        self.O = O

    #rotates the primitive shape by the specified number of degrees in each direction
    def rotate(self, deg_x, deg_y, deg_z):
        print("Not implemented Yet")

    #shifts the primitive in the direction and distance of the vector V
    #def shift(self, V):
    #    self.O = self.O+V

    #adding a vector to a primitive shape will shift the primitive in that direction
    #TODO: DECIDE WHETHER IT SHOULD CHANGE THE VARAIBLE IN THE OBJECT OR RETURN AN ENTIRELY NEW OBJECT
    def __add__(self, v:np.ndarray):
        self.O = self.O+v

    #adding two primitives to each other results in a compound shape that is made out of the two primitive shapes
    def __add__(self):
        return False
        #TODO:IMPLEMENT THIS SHIT

class Cuboid(Primitive):
    
    def __init__(self, O, X, Y, Z):
        super().__init__(O)
        self.X = X
        self.Y = Y
        self.Z = Z

    def set(self, material):

        #If all vectors are orthogonal to each other
        #TODO: FIND OUT IF ORTHOGONAL BY CROSS MULTIPLICATION OF TWO VECTORS
        # SHOULD RETURN THE THIRD VECTOR
        if(np.dot(self.X,self.Y) != 0
        or np.dot(self.X,self.Z) != 0
        or np.dot(self.Y,self.Z) != 0):
            print("Could not set cuboid because vectors are not orthogonal")
            return 0

        #Size of the vector in each direction
        len_X = get_length(self.X)
        len_Y = get_length(self.Y)
        len_Z = get_length(self.Z)

        dir_X = self.X/(len_X*2)
        dir_Y = self.Y/(len_Y*2)
        dir_Z = self.Z/(len_Z*2)

        for a in range(0, int(len_X*2)):
            for b in range(0, int(len_Y*2)):
                for c in range(0, int(len_Z*2)):
                    BasicOperation.set_block(self.O + a*dir_X + b*dir_Y + c*dir_Z, material)


class Sphere(Primitive):
    def __init__(self, O, radius):
        super().__init__(O)
        self.radius = radius

    #Returns the position vector that is a normal on the surface of the sphere pointing in the direction vector
    def normal(direction):
        return []
    
    def set(self,material):
        # pos1 = self.O - [self.radius, self.radius, self.radius]
        pos1 = np.subtract(self.O, [self.radius, self.radius, self.radius])

        for x in range(0,2*self.radius):
            for y in range(0,2*self.radius):
                for z in range(0,2*self.radius):
                    current_pos = pos1 + [x,y,z]

                    if(get_length(self.O - current_pos) <= self.radius):
                        BasicOperation.set_block(current_pos, material)
    

class Cylinder(Primitive):
    #define a cylinder with starting from O and in direction and length defined by V, of given radius
    def __init__(self, O, V, radius):
        super().__init__(O)
        self.V = V
        self.radius = radius
    
    #sets the cylinder out of given material in the game world
    def set(self, material):
        print("TO BE IMPLEMENTED")

