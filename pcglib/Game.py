from mcpi.minecraft import Minecraft
import math

from pcglib.new_buffer import new_buffer

class Game(new_buffer):
    def __init__(self, offset):
        self._x_offset = offset[0]
        self._y_offset = offset[1]
        self._z_offset = offset[2]
        self.mc = Minecraft.create()

    def set(self, pos, id):
        msg = "Set block at ", str(pos[0]) ,", ", str(pos[1]), ",", str(pos[2]), "to ", id
        self.msg(msg)
        self.mc.setBlock(pos[0] + self._x_offset,pos[1] + self._y_offset,pos[2] + self._z_offset, id)

    def get(self, pos):
        return self.mc.getBlock(pos[0] + self._x_offset, pos[1] + self._y_offset, pos[2] + self._z_offset)

    def msg(self, msg):
        self.mc.postToChat(msg)