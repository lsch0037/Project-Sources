from csglib.Game import Game
from csglib.primitive import *
from csglib.buffer import *
# from csglib.material import *
from csglib.compound import *

def main():

    offset_pc = [-144, -81, -224]
    game = Game(offset_pc)

    game.get([0, 1, 0], 1)

if __name__ == "__main__":
    main()