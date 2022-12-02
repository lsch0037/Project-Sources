import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid

O = Zero + [0,70, 0]
O_2 = O + [1,1,1]

X = Vector([10,0,0])
Y = Vector([0,0,10])
Z = Vector([0,10,0])

X_2 = X - [-2, 0, 0]
Y_2 = Y - [0, -2, 0]
Z_2 = Z - [0, 0, -2]

shape1 = Cuboid(O, X, Y, Z, 1)

shape2 = Cuboid(O_2, X_2, Y_2, Z_2, 3)

shape3 = shape1 - shape2

# shape3.carve()
shape1.set()