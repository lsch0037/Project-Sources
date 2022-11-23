from mcpi.minecraft import Minecraft
import numpy as np

from ServerOperations import BasicOperation
from Primitives import Cuboid
import GlobalVariables

mc = GlobalVariables.mc

basicOperations = BasicOperation()

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
    

x,y,z = mc.player.getPos()
O = [x + 10, y, z + 10]

X = [10, 0, 0]
Y = [0, 10, 0]
Z = [0, 0, 10]

basicOperations.set_block(O, 1)

# cbd = Cuboid(0, X, Y, Z)
# cbd.set(1)