import sys
import os
sys.path.append(os.path.abspath('../pcglib'))

import unittest
from vec3 import vec3

class testVectors(unittest.TestCase):
    def testAdd(self):
        A = vec3([3,5,7])
        B = vec3([4,3,2])

        C = A + B

        self.assertEqual(C, [7,8,9])


    def testSub(self):
        A = vec3([3,5,7])
        B = vec3([4,3,2])

        C = A - B

        self.assertTrue(C == [-1,2,5])


    def testCrossProd(self):
        A = vec3([1,0,0])
        B = vec3([0,1,0])

        C = A * B

        self.assertTrue(C == [0,0,1])


    def testDotProd(self):
        A = vec3([3,1,5])

        B = A*3

        self.assertTrue(B == [9,3,15])


    def testDiv(self):
        A = vec3([3,6,9])

        B = A / 3

        self.assertEqual(B, [1,2,3])


    def testLen(self):
        A = vec3([6,3,6])

        len = abs(A)

        self.assertEqual(len, 9)


    def testDir(self):
        A = vec3([6,3,6])

        dir = A.dir()

        self.assertTrue(dir == [2/3, 1/3, 2/3])

if __name__ == '__main__':
    unittest.main()