import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from Compound import PrimitiveNode
from VectorOperations import Vector

O = Zero + [0,70, 0]
O_2 = O + [1,1,1]

shape1 = PrimitiveNode(O, 10, 1)
shape2 = PrimitiveNode(O_2, 8, 1)

shape3 = shape1 - shape2

shape3.set()