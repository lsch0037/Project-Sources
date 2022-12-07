import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid
from Buffer import Buffer
from Buffer import GameBuffer

game = GameBuffer(mc)

x_len,y_len,z_len = 10,10,10

buf1 = Buffer(x_len, y_len, z_len)

buf1.setOrigin(Zero + [0, 70, 0])

buf1.write(game)