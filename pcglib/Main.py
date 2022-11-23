import numpy as np

from Primitives import Cuboid
from GlobalVariables import mc

# mc = GlobalVariables.mc

# class GeometricPrimitiveFunction():

#     def set_line(pos1, pos2, id):

#         direction = np.subtract(pos2,pos1)

#         length = get_length(direction)

#         direction = direction / length

#         current_pos = pos1

#         for a in range(0, int(length)):
#             current_pos = current_pos + direction
#             basicOperations.set_block(mc, current_pos, id)

#     def set_cylinder():
#         print("Set cylinder not programmed yet")
    
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
