from pcglib.Game import Game
from pcglib.vec3 import vec3
from pcglib.mat4 import mat4
from pcglib.primitive import *
from pcglib.buffer import *

# Offset of the server
Zero = vec3([-144.5, -81.5, -224.5])

# Initiating game object
game = Game(Zero)
pos = vec3(0.5,100.5,0.5)

# rot = mat4()
# rot.identity()

# c = cylinder(pos, rot, 1, 6, 10)
# c.set(game)

print(game.ground(0,0))