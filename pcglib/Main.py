from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid
from Primitives import Sphere
from Buffer import Buffer
from Buffer import GameBuffer
from vec3 import vec3
from mat4 import mat4
from new_primitive import new_cube

game = GameBuffer(mc, Zero)

p0 = vec3([0.0,100.0,0.0])
r0 = mat4()
r0.identity()

c = new_cube(p0,r0, 3)
c.set(1, game)