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

m = mat4([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
m2 = mat4()
m2.identity()

print(m*m2)