import sys
import os
sys.path.append(os.path.abspath('../pcglib'))

from buffer import buffer
import unittest

from random import randint

class testBuffer(unittest.TestCase):
    def testGetEmpty(self):
        buf = buffer()

        pos = [randint(-100,100), randint(-100, 100), randint(-100,100)]

        self.assertEqual(buf.get(pos), -1)


    def testGetSet(self):
        buf = buffer()

        pos = [randint(-100,100), randint(-100, 100), randint(-100,100)]
        id = randint(0,100)
        buf.set(pos, id)

        self.assertEqual(buf.get(pos), id)


    def testUnsetSet(self):
        buf = buffer()

        pos = [randint(-100,100), randint(-100, 100), randint(-100,100)]
        id = randint(0,100)
        buf.set(pos, id)
        buf.unset(pos)

        self.assertEqual(buf.get(pos), -1)


    def testUnsetEmpty(self):
        buf = buffer()

        pos = [randint(-100,100), randint(-100, 100), randint(-100,100)]
        buf.unset(pos)

        self.assertEqual(buf.get(pos), -1)


    def testGround(self):
        buf = buffer()
        height_map = []
        size = 100

        for i in range(size):
            height_map.append([])
            for j in range(size):
                height = randint(1, 10)

                pos = [i, height, j]
                buf.set(pos, 1)
                height_map[i].append(height)

        for f in range(10):
            x = randint(0,size)
            z = randint(0,size)

            self.assertEqual(buf.ground(x,z), height_map[x][z])


    def testWriteTo(self):
        buf1 = buffer()
        buf2 = buffer()

        poss = []

        # Add random entries
        for i in range(10):
            pos = [randint(0,10), randint(0,10), randint(0,10)]

            id = randint(0, 10)
            poss.append(pos)

            buf1.set(pos, id)

        # Write buffer
        buf1.write(buf2)

        # Test entries are correct
        for j in range(len(poss)):
            pos = poss[j]
            
            self.assertEqual(buf1.get(pos), buf2.get(pos))


if __name__ == '__main__':
    unittest.main()