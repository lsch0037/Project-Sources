from mcpi.minecraft import Minecraft
import numpy as np

from Primitives import Sphere
from VectorOperations import get_length
from ServerOperations import BasicOperation

mc = Minecraft.create()

basicOperations = BasicOperation(mc)

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
# O = np.array([0.5,100.5,0.5])
O = [x + 10, y, z + 10]


basicOperations.set_block(O, 1)

# cuboid = Sphere(O, 10)
# cuboid.set(1)

#obj1 = Sphere(O, 15)
#obj1.set(0)
