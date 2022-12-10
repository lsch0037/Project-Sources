from Compound import *
import numpy as np
import ServerOperations
from GlobalVariables import Zero
from VectorOperations import Vector
from Buffer import Buffer

# import unittest

class testPcglib(unittest.TestCase):
    def testVectorAdd(self):
        vec1 = Vector([3,5,7])
        vec2 = Vector([4,3,2])

        vec3 = vec1 + vec2

        self.assertEqual(vec3.toList(), [7,8,9])

    def testVectorSub(self):
        vec1 = Vector([3,5,7])
        vec2 = Vector([4,3,2])

        vec3 = vec1 - vec2

        self.assertEqual(vec3.toList(), [-1,2,5])

    def testVectorMul(self):
        vec1 = Vector([1,0,0])
        vec2 = Vector([0,1,0])

        vec3 = vec1 * vec2

        self.assertEqual(vec3.toList(), [0,0,1])

    def testVectorDiv(self):
        vec1 = Vector([3,6,9])

        vec3 = vec1 / 3

        self.assertEqual(vec3.toList(), [1,2,3])


    def testVectorLenght(self):
        vec1 = Vector([6,3,6])

        len = vec1.getLength()

        self.assertEqual(len, 9)

    def testVectorDirection(self):
        vec1 = Vector([6,3,6])

        direction = vec1.getDirection()

        self.assertEqual(direction.toList(), [2/3, 1/3, 2/3])

    def testReplaceBlock(self):
        print("Testing replacing single block")
        O = Zero + [0,100,0]
        ServerOperations.set_block(O, 1)
        
        ServerOperations.set_block(O, 0, replacing=1)
        
        self.assertEqual(ServerOperations.query_block(O), 0)
        print("Passed Test")

    def testReplaceWrongBlock(self):
        print("Testing replacing wrong single block")
        O = Zero + [0,100,0]
        ServerOperations.set_block(O, 1)
        
        ServerOperations.set_block(O, 0, replacing=10)
        
        self.assertEqual(ServerOperations.query_block(O), 1)

        ServerOperations.set_block(O, 0)
        print("Passed Test")

    def testReplaceBlocks(self):
        # TODO: CHANGE TO MULTIPLE BLOCKS
        print("Testing multiple single block")
        O = Zero + [0,100,0]

        ServerOperations.set_block(O, 1)
        
        ServerOperations.set_block(O, 0, replacing=1)
        
        self.assertEqual(ServerOperations.query_block(O),0)
        print("Passed Test")

    def testReplaceWrongBlocks(self):
        # TODO: CHANGE TO MULTIPLE BLOCKS
        print("Testing replacing multiple wrong blocks")
        O = Zero + [0,100,0]
        ServerOperations.set_block(O, 1)
        
        ServerOperations.set_block(O, 0, replacing=10)
        
        self.assertEqual(ServerOperations.query_block(O), 1)

        ServerOperations.set_block(O, 0)
        print("Passed Test")

    def testAddNode(self):
        print("Testing Adding Functionality")
        O = Zero + [10,110,10]

        shape1 = PrimitiveNode(O, 10, 1)

        O_2 = O + [1,1,1]

        shape2 = PrimitiveNode(O_2, 8, 0)

        shape3 = shape1 + shape2

        self.assertEqual(len(shape3.children),2)
        self.assertEqual(shape3.getChild(0), shape1)
        self.assertEqual(shape3.getChild(1), shape2)

        print("Passed Test")

    def testSetAdd(self):
        print("Testing Setting Tree of Additions")
        O = Zero + [10,100,10]
        shape1 = PrimitiveNode(O, 10, 17)
        O_2 = Zero + [-10,100,-10]
        shape2 = PrimitiveNode(O_2, 10, 5)
        shape3 = shape1 + shape2

        shape3.set()

        I = O + [10,10,10]
        blocksShape1 = ServerOperations.query_blocks(O,I)
        I_2 = O_2 + [10,10,10]
        blocksShape2 = ServerOperations.query_blocks(O_2,I_2)

        self.assertEqual(set(blocksShape1), {17})
        self.assertEqual(set(blocksShape2), {5})

        ServerOperations.fill(O, I, 0)
        ServerOperations.fill(O_2, I_2, 0)
        print("Passed Test")

    # def testSetSub(self):
    #     print("Testing Setting Tree of Subtractions")
    #     O = Zero + [10,100,10]
    #     shape1 = PrimitiveNode(O, 10, 17)
    #     O_2 = Zero + [-10,100,-10]
    #     shape2 = PrimitiveNode(O_2, 10, 5)
    #     shape3 = shape1 - shape2

    #     shape3.set()

    #     I = O + [10,10,10]
    #     blocksShape1 = ServerOperations.query_blocks(O,I)
    #     I_2 = O_2 + [10,10,10]
    #     blocksShape2 = ServerOperations.query_blocks(O_2,I_2)

    #     self.assertEqual(set(blocksShape1), {17})
    #     self.assertEqual(set(blocksShape2), {5})

    #     ServerOperations.fill(O, I, 0)
    #     ServerOperations.fill(O_2, I_2, 0)
    #     print("Passed Test")


if __name__ == '__main__':
    unittest.main()