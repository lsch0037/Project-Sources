import unittest

from csglib.compound import *
from csglib.primitive import *
from csglib.material import *

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