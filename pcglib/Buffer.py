import numpy as np
from VectorOperations import Vector

class Buffer():
    def __init__(self, x_0, y_0, z_0, x, y, z):
        x_len = x - x_0
        y_len = y - y_0
        z_len = z - z_0
        
        self._x_0 = x_0
        self._y_0 = y_0
        self._z_0 = z_0

        self._x_1 = x
        self._y_1 = y
        self._z_1 = z

        self._arr = np.zeros((x_len, y_len, z_len))

    def set(self, x,y,z,id):
        self._arr[x - self._x_0][y - self._y_0][z - self._z_0] = id

    def resize(self, x, y, z):
        x_len, y_len, z_len = self._arr.shape

        new_x_0, new_y_0, new_z_0 = self._x_0, self._y_0, self._z_0
        new_x, new_y, new_z = x_len, y_len, z_len


        # if x greater than range
        if x > self._x_0 + x_len:
            new_x = x
        elif x < self._x_0:
            new_x_0 = x

        # if y greater than range
        if y > self._y_0 + y_len:
            new_y = y
        elif y < self._y_0:
            new_y_0 = y

        # if z greater than range
        if z > self._z_0 + z_len:
            new_z = z
        elif z < self._z_0:
            new_z_0 = z

        newBuffer = Buffer(new_x_0, new_y_0, new_z_0, new_x, new_y, new_x)

        self.write(newBuffer)

        return newBuffer

    def setOrigin(self, O):
        self._x_0 = O[0]
        self._y_0 = O[1]
        self._z_0 = O[2]

    def get(self, x, y, z):
        return self._arr[x - self._x_0][y - self._y_0][z - self._z_0]

    def getOrigin(self):
        return [self._x_0, self._y_0, self._z_0]

    def getShape(self):
        return self._arr.shape

    def write(self, other, ignoreAir=True):
        if isinstance(other, Buffer):
            id = 0

            for x in range(self._x_0, self._x_1):
                for y in range(self._y_0, self._y_1):
                    for z in range(self._z_0, self._z_1):
                        id = self.get(x,y,z)

                        if ignoreAir and id == 0:
                            continue
                        
                        other.set(x ,y, z, id)

class GameBuffer(Buffer):
    def __init__(self, mc, Zero):
        self.mc = mc
        self._x_offset = Zero[0]
        self._y_offset = Zero[1]
        self._z_offset = Zero[2]

    def set(self,x,y,z,id):
        msg = "Set block at ", str(x) ,", ", str(y), ",", str(z), "to ", id
        self.mc.postToChat(msg)
        self.mc.setBlock(x + self._x_offset,y + self._y_offset,z + self._z_offset, id)

    def get(self,x,y,z):
        return self.mc.getBlock(x + self._x_offset,y + self._y_offset,z + self._z_offset)
