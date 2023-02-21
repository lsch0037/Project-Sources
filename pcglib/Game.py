from mcpi.minecraft import Minecraft
from Buffer import Buffer

class GameBuffer(Buffer):
    def __init__(self, Zero, x_0=-10, y_0=-10, z_0=-10, x_1=10,y_1=10,z_1=10,):
        super().__init__(x_0,y_0,z_0, x_1, y_1, z_1)
        self._x_offset = Zero[0]
        self._y_offset = Zero[1]
        self._z_offset = Zero[2]
        self.mc = Minecraft.create()

    def set(self, pos, id):
        msg = "Set block at ", str(pos[0]) ,", ", str(pos[1]), ",", str(pos[2]), "to ", id
        self.msg(msg)
        self.mc.setBlock(pos[0] + self._x_offset,pos[1] + self._y_offset,pos[2] + self._z_offset, id)

    def get(self, pos):
        return self.mc.getBlock(pos[0] + self._x_offset, pos[1] + self._y_offset, pos[2] + self._z_offset)

    def msg(self, msg):
        self.mc.postToChat(msg)