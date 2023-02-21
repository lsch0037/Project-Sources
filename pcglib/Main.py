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

p0 = vec3([0.5,100.5,0.5])
r0 = mat4()
r0.identity()
# r0.rotateY(3.0)

material = 0

c = new_cube(p0,r0, 4)
c.set(material, game)