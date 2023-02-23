from pcglib.Game import Game
from pcglib.vec3 import vec3
from pcglib.mat4 import mat4
from pcglib.primitive import *
from pcglib.new_buffer import *

# Offset of the server
Zero = vec3([-144, -81, -224])

# Initiating game object
game = Game(Zero)
pos = vec3(0,100,0)


rot = mat4()
rot.identity()

c = cube(pos, rot, 0, 10)
c.set(game)