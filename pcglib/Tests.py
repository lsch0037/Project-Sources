from Compound import *
import numpy as np
import ServerOperations
from GlobalVariables import Zero

def testAll():
    print("Running All Tests")
    testReplaceBlock()
    testReplaceWrongBlock()
    testReplaceBlocks()
    testReplaceWrongBlocks()
    testAddNode()
    testSetAdd()
    print("Passed All Tests")

def testReplaceBlock():
    print("Testing replacing single block")
    O = np.add(Zero, [0,100,0])
    ServerOperations.set_block(O, 1)
    
    ServerOperations.set_block(O, 0, replacing=1)
    
    assert ServerOperations.query_block(O) == 0
    print("Passed Test")

def testReplaceWrongBlock():
    print("Testing replacing wrong single block")
    O = np.add(Zero, [0,100,0])
    ServerOperations.set_block(O, 1)
    
    ServerOperations.set_block(O, 0, replacing=10)
    
    assert ServerOperations.query_block(O) == 1

    ServerOperations.set_block(O, 0)
    print("Passed Test")

def testReplaceBlocks():
    # TODO: CHANGE TO MULTIPLE BLOCKS
    print("Testing multiple single block")
    O = np.add(Zero, [0,100,0])
    ServerOperations.set_block(O, 1)
    
    ServerOperations.set_block(O, 0, replacing=1)
    
    assert ServerOperations.query_block(O) == 0
    print("Passed Test")

def testReplaceWrongBlocks():
    # TODO: CHANGE TO MULTIPLE BLOCKS
    print("Testing replacing multiple wrong blocks")
    O = np.add(Zero, [0,100,0])
    ServerOperations.set_block(O, 1)
    
    ServerOperations.set_block(O, 0, replacing=10)
    
    assert ServerOperations.query_block(O) == 1

    ServerOperations.set_block(O, 0)
    print("Passed Test")

def testAddNode():
    print("Testing Adding Functionality")
    O = np.add(Zero, [10,110,10])

    shape1 = PrimitiveNode(O, 10, 1)

    O_2 = np.add(O, [1,1,1])

    shape2 = PrimitiveNode(O_2, 8, 0)

    shape3 = shape1 + shape2

    assert len(shape3.children) == 2
    assert shape3.getChild(0) == shape1
    assert shape3.getChild(1) == shape2

    print("Passed Test")

def testSetAdd():
    print("Testing Setting Tree of Additions")
    O = np.add(Zero, [10,100,10])
    shape1 = PrimitiveNode(O, 10, 17)
    O_2 = np.add(Zero, [-10,100,-10])
    shape2 = PrimitiveNode(O_2, 10, 5)
    shape3 = shape1 + shape2

    shape3.set_traverse()

    I = np.add(O, [10,10,10])
    blocksShape1 = ServerOperations.query_blocks(O,I)
    I_2 = np.add(O_2, [10,10,10])
    blocksShape2 = ServerOperations.query_blocks(O_2,I_2)

    assert set(blocksShape1) == {17}
    assert set(blocksShape2) == {5}

    ServerOperations.fill(O, I, 0)
    ServerOperations.fill(O_2, I_2, 0)
    print("Passed Test")

testAll()