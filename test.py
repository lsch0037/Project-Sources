from scipy.ndimage import rotate

from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.buffer import *
from pcglib.material import *
from pcglib.compound import *

from perlin_noise import PerlinNoise

# Offset of the server
offset_pc = [-144, -81, -224]

# Server on Laptop
offset_laptop = [-95.0, -65.0, -63.0]

# Initiating game object
game = Game(offset_pc)

pos1 = np.array([0.0,63.0,0.0])
pos2 = np.array([10.0,63.0,10.0])
orientation = np.identity(3)

mat = random_material(["Stone"])

cb = cuboid(pos1, orientation, mat,[10,10,10])
cb2 = cuboid(pos2, orientation, mat, [10,10,10])

union = cb + cb2
buf = union.set()

buf.write(game)

print("Bounding Box:", buf)