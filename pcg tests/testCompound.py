import sys
import os
import unittest
import random

sys.path.append(os.path.abspath('../pcglib'))

from compound import *
from primitive import *
from material import *
import numpy as np

# GLOBALS
testMaterial = random_material(["Stone"])
testOrientation = np.identity(3)
testPos = np.array([0.0, 80.0, 0.0])


class testCompound(unittest.TestCase):
    def testDifference(self):
        global testMaterial
        global testOrientation
        global testPos

        c = cylinder(testMaterial, 5, 10)
        s = sphere(testMaterial , 7)

        diff = differenceNode([c, s])

        buf = diff.set(testPos, testOrientation)

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()