from Game import GameBuffer
from vec3 import vec3
from mat4 import mat4
from primitive import *

# Offset of the server
Zero = vec3([-144, -81, -224])

# Initiating game object
game = GameBuffer(Zero)

p0 = vec3([0.5,100.5,0.5])
r0 = mat4()
r0.identity()
# r0.rotateY(3.0)

material = 0

c = cube(p0,r0, 4)
c.set(material, game)

s = sphere(p0,r0, 4)