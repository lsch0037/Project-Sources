import csglib.Game
import csglib.material
import csglib.primitive
import csglib.compound

import numpy as np

zero_pc = np.array([-144, -81, -224])
mc = csglib.Game.Game(zero_pc)


mat = csglib.material.random_material(["Stone"])

shape1 = csglib.primitive.sphere(mat, 10)
shape2 = csglib.primitive.cube(mat, 10)


compound1 = csglib.compound.prepositionNode("West", [shape2, shape1])

print(compound1.getBounds())

buf = compound1.set(np.array([50, 90,50]), np.identity(3))

buf.write(mc)