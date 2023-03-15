from scipy.ndimage import rotate

from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.buffer import *

# Offset of the server
Zero = [-144, -81, -224]

# Initiating game object
game = Game(Zero)

orientation = np.identity(3)

cb = cube([0,game.getHeight(0,0)+1,0],orientation, 1, 10)
cb.rotateX(45)
cb.set(game)
