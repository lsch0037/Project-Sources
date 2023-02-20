import numpy as np

from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid
from Primitives import Sphere
from Buffer import Buffer
from Buffer import GameBuffer
from vec3 import vec3

game = GameBuffer(mc, Zero)

# height = game.get_ground_height(19,-17)

a = vec3(1,2,3)

cbd = Cuboid(a, )