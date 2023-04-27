import unittest

import random 
import numpy as np

from csglib import compound
from csglib import primitive
from csglib import material

m = material.random_material(["Stone"])

class testBoundingBox(unittest.TestCase):
    def testCube(self):
        size = random.randint(1,10)

        cb = primitive.cube(m, size)

        min, max = cb.getBounds()

        for dim in range(3):
            self.assertEqual(min[dim], 0)
            self.assertEqual(max[dim], size)

    def testCuboid(self):