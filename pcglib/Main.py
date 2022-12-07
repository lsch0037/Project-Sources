import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid
from Buffer import Buffer
from Buffer import GameBuffer

game = GameBuffer(mc, Zero)

buf1 = Buffer(10,10,10, 10,10,10)

print(buf1.getShape())

for i in range(0,10):
    buf1.set(i, i, i, 1)

buf2 = buf1.resize(0,0,0, 20,20,20)

print(buf2.getShape())

print(buf2._arr)

# buf1.write(game)
# game.set(0, 100,0, 1)

# buf1.set(0, 69, 0, 1)

# print(buf1.get(0, 69, 0))
