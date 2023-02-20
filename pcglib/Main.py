import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid
from Primitives import Sphere
from Buffer import Buffer
from Buffer import GameBuffer

game = GameBuffer(mc, Zero)

height = game.get_ground_height(19,-17)
