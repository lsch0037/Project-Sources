from scipy.ndimage import rotate

from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.buffer import *
from pcglib.material import *

# Offset of the server
offset_pc = [-144, -81, -224]

# Server on Laptop
offset_laptop = [-95.0, -65.0, -63.0]

# Initiating game object
game = Game(offset_pc)

position = np.array([0.0,100.0,0.0])
orientation = np.identity(3)

mat = material([1,2,3],selector='rand')

sp = sphere(position, mat,10)

sp.set(game)