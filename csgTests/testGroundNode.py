import sys
import os
sys.path.append(os.path.abspath('/csglib'))

from csglib.Game import Game
from csglib.primitive import *
from csglib.buffer import *
from csglib.material import *
from csglib.compound import *

# Offset of the server
offset_pc = [-144, -81, -224]

# Server on Laptop
offset_laptop = [-95.0, -65.0, -63.0]

# Initiating game object
game = Game(offset_pc)

pos1 = np.array([0.0,80.0,0.0])
# pos2 = np.array([10.0, 80.0, 0.0])
orientation = np.identity(3)

mat = random_material(["Stone"])

cb1 = cube(mat,5)

cmp = onGroundNode(game, [cb1])

buf = cmp.set(pos1, orientation)

buf.write(game)