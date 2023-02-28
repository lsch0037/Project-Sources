from Game import *
from vec3 import vec3
from mat4 import mat4
from primitive import *
from buffer import *

# Offset of the server
Zero = vec3([-142, -81, -223])

# Initiating game object
game = Game(Zero)
pos = vec3(0,100,0)

print(game.get(pos))
game.set(pos, 1)

print(game.get(pos))