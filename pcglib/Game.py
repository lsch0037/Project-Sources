from mcpi.minecraft import Minecraft
import math

from pcglib.buffer import buffer

class Game(buffer):
    def __init__(self, offset):
        # self._x_offset = offset[0]
        # self._y_offset = offset[1]
        # self._z_offset = offset[2]
        self.offset = offset
        self.mc = Minecraft.create()

    def set(self, pos, id):
        msg = "Set block at ", str(pos[0]) ,", ", str(pos[1]), ",", str(pos[2]), "to ", id
        self.msg(msg)
        self.mc.setBlock(pos[0] + self.offset[0],pos[1] + self.offset[1],pos[2] + self.offset[2], id)

    def get(self, pos):
        print("Getting:", pos)
        return self.mc.getBlock(pos[0] + self.offset[0], pos[1] + self.offset[1], pos[2] + self.offset[2])

    def msg(self, msg):
        self.mc.postToChat(msg)