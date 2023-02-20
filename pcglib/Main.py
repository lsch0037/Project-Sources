from GlobalVariables import mc
from GlobalVariables import Zero
from VectorOperations import Vector
from Primitives import Cuboid
from Primitives import Sphere
from Buffer import Buffer
from Buffer import GameBuffer
from vec3 import vec3
from mat4 import mat4

game = GameBuffer(mc, Zero)

v = vec3(1,2,3)
v2 = v.clone() - [5,6,7]

print(v)
print(v2)
print(v+v2)