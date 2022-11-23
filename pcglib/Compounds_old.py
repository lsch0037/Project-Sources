import numpy as np
from Primitives import Primitive
from VectorOperations import get_length
from ServerOperations import BasicOperation

#Compound shape that is a tree of primitives
class Compound():
    # def __init__(self, primitives):
    #     self.primitives = primitives

    #Add a new primitive shape to the current compound shape 
    def add(self, primitive):
        # add to the tree
        print("TO BE IMPLEMENTED")

    #sets all the primitives inside the current compound shape
    def set(self):
        print("TO BE IMPLEMENTED")

    #rotates all the shapes in the compound shape by the specified amount 
    def rotate(self, deg_x, deg_y, deg_z):
        print("TO BE IMPLEMENTED")

    #shifts all primitives in the compound shape in the direction and distance of the vector V
    def shift(self, V):
        self.O = self.O+V

class Node():
    def __init__():
        children = []