import numpy as np
from VectorOperations import Vector

class Buffer():
    def __init__(self, x_0=0, y_0=0, z_0=0, x_len=10, y_len=10, z_len=10):
        self._x_0 = x_0
        self._y_0 = y_0
        self._z_0 = z_0

        self._x_1 = x_0 + x_len
        self._y_1 = y_0 + y_len
        self._z_1 = z_0 + z_len

        self._arr = np.zeros((x_len, y_len, z_len))

    def set(self, x,y,z, material):
        self._arr[int(x)][int(y)][int(z)] = material

    def setAbs(self, x,y,z, material):
        self._arr[self._x_0 - int(x)][self._y_0 - int(y)][self._z_0 - int(z)] = material
        # self._arr[self._x_0 + x][self._y_0 + y][self._z_0 + z] = material

    def resize(self, x_0, y_0, z_0, x,y,z):

        newBuffer = Buffer(x_0, y_0, z_0, x, y, z)

        len_x = self._x_1 - self._x_0
        len_y = self._y_1 - self._y_0
        len_z = self._z_1 - self._z_0

        dx_0 = self._x_0 + x_0
        dy_0 = self._y_0 + y_0
        dz_0 = self._z_0 + z_0

        for i in range(0, len_x):
            for j in range(0, len_y):
                for k in range(0, len_z):
                    newBuffer._arr[dx_0 + i][dy_0 + j][dz_0 + k] = self._arr[i][j][k]

        return newBuffer

    def get(self, x, y, z):
        return self._arr[x][y][z]

    def getAbs(self, x, y, z):
        # return self._arr[x][y][z]
        return self._arr[self._x_0 - x][self._y_0 - y][self._z_0 - z]

    def getPos0(self):
        return self._x_0, self._y_0, self._z_0

    def getPos1(self):
        return self._x_1, self._y_1, self._z_1

    def shiftOrigin(self, x, y, z):
        self._x_0 += x
        self._y_0 += y
        self._z_0 += z

        self._x_1 += x
        self._y_1 += y
        self._z_1 += z

    def getShape(self):
        return self._arr.shape

    def write(self, other):
        # if not self.isSubsetOf(other):
        #     print("other buffer must be subset of this buffer")
        #     return

        id = 0
        for x in range(self._x_0, self._x_1):
            for y in range(self._y_0, self._y_1):
                for z in range(self._z_0, self._z_1):
                    # print(x,y,z)
                    id = self.getAbs(x,y,z)
                    other.set(x ,y, z, id)

    def isSubsetOf(self, other):
        other_x_0, other_y_0, other_z_0 = other.getPos0()
        other_x_1, other_y_1, other_z_1 = other.getPos1()

        if self._x_0 < other_x_0 or self._y_0 < other_y_0 or self._z_0 < other_z_0:
            return False
        elif self._x_1 > other_x_1 or self._y_1 > other_y_1 or self._z_1 > other_z_1:
            return False

        return True

    def __GT__(self, other):
        if self._x_0 > other._x_0 or self._y_0 > other._y_0 or self._z_0 > other._z_0:
            return False
        elif self._x_1 < other._x_1 or self._y_1 < other._y_1 or self._z_1 < other._z_1:
            return False

        return True

class GameBuffer(Buffer):
    def __init__(self, mc, Zero, x_0=0, y_0=0, z_0=0, x_len=10, y_len=10, z_len=10):
        super().__init__(x_0,y_0,z_0, x_len,y_len,z_len)
        self._x_offset = Zero[0]
        self._y_offset = Zero[1]
        self._z_offset = Zero[2]
        self.mc = mc

    def set(self,x,y,z,id):
        msg = "Set block at ", str(x) ,", ", str(y), ",", str(z), "to ", id
        self.mc.postToChat(msg)
        self.mc.setBlock(x + self._x_0 + self._x_offset,y + self._y_0 + self._y_offset,z + self._z_0 + self._z_offset, id)

    def get(self,x,y,z):
        return self.mc.setBlock(x + self._x_0 + self._x_offset,y + self._y_0 + self._y_offset,z + self._z_0 + self._z_offset)
