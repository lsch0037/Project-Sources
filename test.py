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

mat = material([1,3,16,15,56],selector='perlin', weights=[0.5,0.2,0.15, 0.1, 0.05], octaves=12)
mat2 = material([20,49],selector='perlin', weights=[0.5,0.5], octaves=8, seed=random.randint(100,10000))

mat3 = material([0],selector='rand')

# sp = sphere(position, mat2,10)
cb = cuboid(position, orientation, mat3,[20,20,20])

cb.set(game)