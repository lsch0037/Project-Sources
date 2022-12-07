import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid
from Buffer import Buffer
from Buffer import GameBuffer

game = GameBuffer(mc, Zero)


buf1 = Buffer(0,60,0, 10,70,10)

len_x, len_y, len_z = buf1.getShape()

buf1.set(0, 69, 0, 1)

print(buf1.get(0, 69, 0))

buf1.write(game)