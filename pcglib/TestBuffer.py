import unittest
from random import randint

from Buffer import Buffer

class TestBuffer(unittest.TestCase):
    def testSet(self):
        buf = Buffer(100,100,100, 200,200,200)

        for i in range(0,10):
            rand_x = randint(100,200)
            rand_y = randint(100,200)
            rand_z = randint(100,200)

            buf.set(rand_x, rand_y, rand_z, 1)
            self.assertEqual(buf.get(rand_x, rand_y, rand_z),1)

    def testWrite(self):
        buf1 = Buffer()
        buf2 = Buffer()

        for i in range(0,10):
            rand_x = randint(-10, 10)
            rand_y = randint(-10, 10)
            rand_z = randint(-10, 10)

            buf1.set(rand_x, rand_y, rand_z, 1)
            buf1.write(buf2)

            self.assertEqual(buf2.get(rand_x, rand_y, rand_z), 1)
        
    def testBufResizeSmallerPos0(self):
        for i in range(0,10):
            buf = Buffer(0,0,0, 10,10,10)

            rand_x = randint(0, 10)
            rand_y = randint(0, 10)
            rand_z = randint(0, 10)

            buf.set(rand_x, rand_y, rand_z, 1)

            buf.resize(-10,-10,-10, 10,10,10)

            self.assertEqual(buf.getPos0(), (-10,-10,-10))
            self.assertEqual(buf.getPos1(), (10,10,10))
            self.assertEqual(buf.getShape(), (21,21,21))

            self.assertEqual(buf.get(rand_x, rand_y, rand_z), 1)

    def testBufResizeGreaterPos1(self):
        for i in range(0,10):
            buf = Buffer(-10,-10,-10, 0,0,0)

            rand_x = randint(-10, 0)
            rand_y = randint(-10, 0)
            rand_z = randint(-10, 0)

            buf.set(rand_x, rand_y, rand_z, 1)

            buf.resize(-10,-10,-10, 10,10,10)

            self.assertEqual(buf.getPos0(), (-10,-10,-10))
            self.assertEqual(buf.getPos1(), (10,10,10))

            self.assertEqual(buf.get(rand_x, rand_y, rand_z), 1)

    # TODO: TEST GAME BUFFER

if __name__ == '__main__':
    unittest.main()