import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid
from Primitives import Sphere
from Buffer import Buffer
from Buffer import GameBuffer

game = GameBuffer(mc, Zero)

buf1 = Buffer(0,0,0, 20,20,20)

O = Vector([10,10,10])
O_2 = Vector([0,0,0])

X = Vector([15,0,0])
Y = Vector([0,15,0])
Z = Vector([0,0,15])

cbd = Cuboid(O_2, X,Y,Z, 3)
spr1 = Sphere(O, 5, 1)

shape = cbd + spr1

shape.set(buf1)
print(buf1._arr)

buf1.shiftOrigin(0, 100, 0)
buf1.write(game)

# buf1.write(game)
# game.set(0, 100,0, 1)

# buf1.set(0, 69, 0, 1)

# print(buf1.get(0, 69, 0))
