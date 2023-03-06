from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.buffer import *

# Offset of the server
Zero = [-144, -81, -224]

# Initiating game object
game = Game(Zero)
pos1 = np.array([0.5,game.ground(0.5,0.5),0.5])
pos2 = pos1 + np.array([0.0,5.0,0.0])

rot = np.identity(3)

cb1 = cube(pos1, rot, 1, 10)
cb2 = cube(pos2, rot, 1, 5)

tree = cb1 - cb2

tree.set(game)

# cb1.set(game)