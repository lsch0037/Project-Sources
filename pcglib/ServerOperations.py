from mcpi.minecraft import Minecraft

class BasicOperation():
    def __init__(self, mc):
        self.mc = mc

    def set_block(self, pos, id):
        self.mc.setBlock(pos[0], pos[1], pos[2], id)

    #Sets a rectangle between corners pos1 and pos2 to block with given id
    def fill(self, pos1, pos2, id):
        self.mc.setBlocks(pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2], id)

    def query_block(self, pos):
        return self.mc.getBlock(pos[0], pos[1], pos[2])

    def query_blocks(self, pos1, pos2):
        return self.mc.getBlocks(pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2])
