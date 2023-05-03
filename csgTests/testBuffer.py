import unittest
import random

from csglib.buffer import buffer

class testBuffer(unittest.TestCase):
    def testGet(self):
        buf = buffer()

        positions = []
        ids = []

        # Add random entries in the buffer
        for i in range(100):
            pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
            id = random.randint(0,100)
            buf.set(pos, id)

            positions.append(pos)
            ids.append(id)


        # Repeat 100 times
        for i in range(100):
            # Position in the buffer
            if random.randint(0,1) == 0:
                # Select random position from positions added
                index = random.randint(0, len(positions))
                pos = positions[index]
                id = ids[index]

                # Assert the id is the one added
                self.assertEqual(buf.get(pos), id)
            
            # Position not in buffer
            else:

                # Generate random position not added
                while True:
                    pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
                    
                    if not pos in positions:
                        break

                # Assert position is not in buffer
                self.assertEqual(buf.get(pos), None)


    def testUnsetSet(self):
        buf = buffer()

        pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
        id = random.randint(0,100)
        buf.set(pos, id)
        buf.unset(pos)

        self.assertEqual(buf.get(pos), None)


    def testUnsetEmpty(self):
        buf = buffer()

        pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
        buf.unset(pos)

        self.assertEqual(buf.get(pos), None)

    def testWrite(self):
        buf1 = buffer()
        buf2 = buffer()


        positions = []
        ids = []

        # Add random entries to buffer 1
        for i in range(100):
            pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
            id = random.randint(0,100)
            buf1.set(pos, id)

            positions.append(pos)
            ids.append(id)

        # Add random entries to buffer 2
        for i in range(100):
            pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
            id = random.randint(0,100)
            buf2.set(pos, id)

            positions.append(pos)
            ids.append(id)


        # Write buffer 2 to buffer 1
        buf2.write(buf1)


        # Test that all entries exist in buffer 1
        for index in range(len(positions)-1):
            pos = positions[index]
            id = ids[index]
            
            self.assertEqual(buf1.get(pos), id)

    def testUnwrite(self):
        buf1 = buffer()
        buf2 = buffer()

        positions_set = []
        positions_unset = []
        ids = []

        # Add random entries to buffer 1
        for i in range(100):
            pos = [random.randint(-100,100), random.randint(-100, 100), random.randint(-100,100)]
            id = random.randint(0,100)
            buf1.set(pos, id)

            positions_set.append(pos)
            ids.append(id)

        # Add a subset of those entries in buffer 2
        for i in range(50):
            index = random.randint(0, len(positions_set)-1)
            pos = positions_set[index]
            id = positions_set[index]

            buf2.set(pos, id)

            positions_unset.append(pos)

        # Write buffer 2 to buffer 1
        buf2.unwrite(buf1)

        # Test that all entries exist in buffer 1
        for index in range(len(positions_set)-1):
            pos = positions_set[index]
            id = ids[index]

            if pos in positions_unset:
                self.assertEqual(buf1.get(pos), None)
            else:
                self.assertEqual(buf1.get(pos), id)