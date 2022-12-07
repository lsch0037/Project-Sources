import numpy as np
from VectorOperations import Vector

class Buffer():
    def __init__(self, x_size, y_size, z_size, O=[0,0,0]):
        self._arr = np.zeros((x_size,y_size,z_size))
        self.setOrigin(O)

    def set(self, x,y,z,id):
        self._arr[x][y][z] = id

    def setOrigin(self, O):
        if isinstance(O, Vector):
            self._O = O.toList()
        else:
            self._O = O

    def get(self, x, y, z):
        return self._arr[x][y][z]

    def getOrigin(self):
        return self._O

    def write(self, other, ignoreAir=True):
        if isinstance(other, Buffer):
            x_len, y_len, z_len = self._arr.shape

            id = 0

            for x in range(0,x_len):
                for y in range(0,y_len):
                    for z in range(0,z_len):
                        id = self.get(x,y,z)

                        if ignoreAir and id == 0:
                            continue
                        
                        other.set(x + self._O[0],y + self._O[1],z + self._O[2], id)

class GameBuffer(Buffer):
    def __init__(self, mc):
        self.mc = mc

    def set(self,x,y,z,id):
        # msg = "Set block at ", str(x) ,", ", str(y), ",", str(z), "to ", 0
        # self.mc.postToChat(msg)
        self.mc.setBlock(x,y,z, id)

    def get(self,x,y,z):
        return self.mc.getBlock(x,y,z)
