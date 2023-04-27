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
        dim = []
        for i in range(3):
            dim.append(random.randint(1,10))
        
        cb = primitive.cuboid(m, dim)

        min, max = cb.getBounds()

        for i in range(3):
            self.assertEqual(min[i],0)
            self.assertEqual(max[i],dim[i])

    def testSphere(self):
        pass

    def testCylinder(self):
        pass

    def testPyramid(self):
        pass

    def testPrism(self):
        pass

    def testCone(self):
        pass

    # !Compound
    def testOffset(self):
        pass

    def testUnion(self):
        pass

    def testDifference(self):
        pass

    def testIntersection(self):
        pass

    def testOnGround(self):
        pass

    def testShift(self):
        pass

    def testRotation(self):
        pass