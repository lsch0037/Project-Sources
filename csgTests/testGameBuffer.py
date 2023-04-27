import unittest

from csglib.Game import Game

from random import randint

# GLOBALS
Zero = [-144, -81, -224]

game = Game(Zero)

class testGamebuffer(unittest.TestCase):
    def clear(self):
        global game

        for i in range(1000,1010):
            for j in range(100,110):
                for k in range(1000,1010):
                    game.set([i,j,k], 0)


    def setUp(self):
        global game
        game = Game(Zero)
        self.clear()


    def tearDown(self):
        global game
        self.clear()
        del game

    def testGetSet(self):
        global game

        pos = [randint(1000,1010), randint(100,110), randint(1000,1010)]
        id = randint(0,10)
        game.set(pos, id)

        self.assertEqual(game.get(pos), id)

    def testGround(self):
        global game

        # setting coordinates of the point
        x = randint(1000,1010)
        z = randint(1000,1010)

        # setting height
        height = randint(100, 110)

        # settting all blocks below and including height
        for i in range(100, height+1):
            game.set([x,i,z], 1)

        # removing all blocks above height
        for i in range(height+1, 255):
            game.set([x,i,z], 0)        

        self.assertEqual(game.ground(x,z), height)
            
    def testWriteToGame(self):
        global game
        

        # setting coordinates of the point
        x = randint(1000,1010)
        z = randint(1000,1010)

        # setting height
        height = randint(100, 110)

        # settting all blocks below and including height
        for i in range(100, height+1):
            game.set([x,i,z], 1)

        # removing all blocks above height
        for i in range(height+1, 255):
            game.set([x,i,z], 0)        

        self.assertEqual(game.ground(x,z), height)