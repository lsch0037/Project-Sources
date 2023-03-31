from scipy.ndimage import rotate

from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.buffer import *
from pcglib.material import *

from perlin_noise import PerlinNoise

# Offset of the server
offset_pc = [-144, -81, -224]

# Server on Laptop
offset_laptop = [-95.0, -65.0, -63.0]

# Initiating game object
game = Game(offset_pc)

position = np.array([0.0,63.0,0.0])
orientation = np.identity(3)

buf = buffer()

mat = random_material(["Stone"])

cb = cuboid(position, orientation, mat,[10,10,10])

bounding_box = cb.set(buf)
# print("Bounding_box", bounding_box.max, bounding_box.min)
print("Bounding Box:", bounding_box)