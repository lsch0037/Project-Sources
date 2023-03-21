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

position = np.array([0.0,100.0,0.0])
orientation = np.identity(3)

mat = material([1,3,16,15,56],selector='perlin', weights=[0.5,0.2,0.15, 0.1, 0.05])

sp = sphere(position, mat,10)

# nosie = PerlinNoise()
# for i in range(0,10):
#     print("Noise:",nosie([i/10,0/10]))

sp.set(game)