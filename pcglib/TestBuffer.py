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
        

    def testBufResizeGreaterPos0(self):
        buf = Buffer(0,0,0,10,10,10)

        buf.set(5,5,5, 1)

        buf.resize(-10,-10,-10, 10,10,10)

        x_0, y_0, z_0 = buf.getPos0()
        x_1, y_1, z_1 = buf.getPos1()

        self.assertEqual(buf.getPos0(), (-10,-10,-10))
        self.assertEqual(buf.getPos1(), (10,10,10))

        for x in range(x_0, x_1):
            for y in range(y_0, y_1):
                for z in range(z_0, z_1):
                    if x == 5 and y == 5 and z == 5:
                        self.assertEqual(buf.get(x,y,z), 1)
                    else:
                        self.assertEqual(buf.get(x,y,z), 0)

if __name__ == '__main__':
    unittest.main()