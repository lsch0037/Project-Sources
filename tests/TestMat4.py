import sys
import os
sys.path.append(os.path.abspath('../pcglib'))

import unittest
from mat4 import mat4

class testMatrix(unittest.TestCase):
    def testAdd(self):
        pass

    def testSub(self):
        pass

    def testSub(self):
        pass

    def testRotX(self):
        m = mat4()
        m.identity()

        m.rotateX(0.1)

        print(m)

        # self.assertTrue(False)


    def testRotY(self):
        pass

    def testRotZ(self):
        pass

    def testMatMul(self):
        pass

    def testVecMul(self):
        pass

    def testScale(self):
        pass

    def testTranslate(self):
        pass

    def testTranspose(self):
        pass

    def testIdentity(self):
        pass

if __name__ == '__main__':
    unittest.main()