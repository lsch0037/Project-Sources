import unittest
import random

from csglib.buffer import buffer

class testBuffer(unittest.TestCase):
    def testGetEmpty(self):
        buf = buffer()

        pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]

        self.assertEqual(buf.get(pos), -1)


    def testGetSet(self):
        buf = buffer()

        pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
        id = random.randint(0,100)
        buf.set(pos, id)

        self.assertEqual(buf.get(pos), id)


    def testUnsetSet(self):
        buf = buffer()

        pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
        id = random.randint(0,100)
        buf.set(pos, id)
        buf.unset(pos)

        self.assertEqual(buf.get(pos), -1)


    def testUnsetEmpty(self):
        buf = buffer()

        pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
        buf.unset(pos)

        self.assertEqual(buf.get(pos), -1)

    def testWriteTo(self):
        buf1 = buffer()
        buf2 = buffer()

        poss = []

        # Add random entries
        for i in range(10):
            pos = [random.randint(0,10), random.randint(0,10), random.randint(0,10)]

            id = random.randint(0, 10)
            poss.append(pos)

            buf1.set(pos, id)

        # Write buffer
        buf1.write(buf2)

        # Test entries are correct
        for j in range(len(poss)):
            pos = poss[j]
            
            self.assertEqual(buf1.get(pos), buf2.get(pos))

    def testUnwrite(self):
        buf1 = buffer()
        buf2 = buffer()

        poss = [[random.randint(0,10), random.randint(0,10), random.randint(0,10)] for i in range(10)]

        # Add random entries
        for pos in poss:
            buf1.set(pos, 1)
        
        w = 1 / len(poss)
        weights = [w for i in range(len(poss))]
        poss2 = random.choices(poss, weights=weights, k=4)

        for pos in poss2:
            buf2.set(pos, 1)

        buf2.unwrite(buf1)

        for pos in poss:
            if pos in poss2:
                self.assertEqual(buf1.get(pos), -1)
            else:
                self.assertEqual(buf1.get(pos), 1)