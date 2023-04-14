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

pos1 = np.array([0.0,80.0,0.0])
orientation = np.identity(3)

mat = random_material(["Glass"])

cb = cube(mat, 10)
sp = sphere(mat, 5)

buf = cb.set(pos1, orientation)

north = buf.getNorth()
south = buf.getSouth()
east = buf.getEast()
west = buf.getWest()

buf.set(north, 133)
buf.set(south, 57)
buf.set(east, 133)
buf.set(west, 133)

# print("Buf:{}".format(buf))

print("North:{n}, South:{s}, East:{e}, West:{w}".format(n=north, s=south, e= east, w=west))

buf.write(game)