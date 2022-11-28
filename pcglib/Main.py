import numpy as np

from Primitives import Cuboid
from GlobalVariables import mc

# mc = GlobalVariables.mc

Zero = [-143, 19, -223]
O = np.add(Zero,[10, 10, 10])

X = [10, 0, 0]
Y = [0, 10, 0]
Z = [0, 0, 10]

# basicOperations.set_block(O, 1)

# cbd = Cuboid(Zero, X, Y, Z)
# cbd.set(1)


BaseOuter = Cuboid(O, X, Y, Z)
BaseInner = Cuboid(O, X, Y, Z)
BaseInnerT = BaseInner * []
Base = Compound.sub(BaseOuter - BaseInner)
