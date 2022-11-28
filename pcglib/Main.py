import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from Compound import PrimitiveNode
from VectorOperations import Vector

O = Zero + [0,70, 0]
O_2 = O + [1,1,1]

groundFloor = PrimitiveNode(O, 10, 5)
groundFloorHollow = PrimitiveNode(O_2, 8, 1)

