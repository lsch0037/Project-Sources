from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.buffer import *

# Offset of the server
Zero = [-144, -81, -224]

# Initiating game object
game = Game(Zero)

print(game.matchSquare(0,0,10,5))
