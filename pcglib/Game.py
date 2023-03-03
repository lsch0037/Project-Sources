from mcpi.minecraft import Minecraft

from pcglib.buffer import buffer

class Game(buffer):
    def __init__(self, offset):
        self.offset = offset
        self.mc = Minecraft.create()

    def set(self, pos, id):
        # msg = "Set ",pos,  "to ", id
        # print(msg)
        # self.msg(msg)
        
        self.mc.setBlock(pos[0] + self.offset[0],pos[1] + self.offset[1],pos[2] + self.offset[2], id)

    def get(self, pos):

        id = self.mc.getBlock(pos[0] + self.offset[0], pos[1] + self.offset[1], pos[2] + self.offset[2])

        # msg = "Got ",pos, ": ",id
        # print(msg)
        # self.msg(msg)

        return id

    def msg(self, msg):
        self.mc.postToChat(msg)
    
    def write(self, other):
        return