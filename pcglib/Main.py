from Game import *
from vec3 import vec3
from mat4 import mat4
from primitive import *
from new_buffer import *

# Offset of the server
Zero = vec3([-144, -81, -224])

# Initiating game object
# game = GameBuffer(Zero)
game = new_buffer(Zero)
pos = vec3(0,1,2)

game.set(pos, 1)

print(game.get(pos))