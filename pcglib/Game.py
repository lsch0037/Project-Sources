from mcpi.minecraft import Minecraft

from pcglib.buffer import buffer

class Game(buffer):
    def __init__(self, offset):
        self.offset = offset
        self.mc = Minecraft.create()

    def set(self, pos, id):
        self.msg("Set {pos} -> {id}".format(pos=pos, id = id))
        self.mc.setBlock(pos[0] + self.offset[0],pos[1] + self.offset[1],pos[2] + self.offset[2], id)

    def unset(self, pos):
        self.msg("Unset {pos} -> {id}".format(pos=pos, id = id))
        self.mc.setBlock(pos[0] + self.offset[0],pos[1] + self.offset[1],pos[2] + self.offset[2], 0)

    def get(self, pos):
        return self.mc.getBlock(pos[0] + self.offset[0], pos[1] + self.offset[1], pos[2] + self.offset[2])

    def msg(self, msg):
        self.mc.postToChat(msg)
    
    def write(self, other):
        return