import numpy as np

from Primitives import Cuboid
from GlobalVariables import mc
from GlobalVariables import Zero
import ServerOperations

O = np.add(Zero,[0, 101, 0])
I = np.add(O, [10,10,10])

X = [10, 0, 0]
Y = [0, 10, 0]
Z = [0, 0, 10]

ServerOperations.fill(O,I,0, replacing=1)