import numpy as np
from VectorOperations import Vector

class Buffer():
    def __init__(self, x_0=-10, y_0=-10, z_0=-10, x_1=10, y_1=10, z_1=10):
        self._x_0 = x_0
        self._y_0 = y_0
        self._z_0 = z_0

        self._x_1 = x_1
        self._y_1 = y_1
        self._z_1 = z_1

        self._arr = np.zeros((x_1 - x_0 + 1, y_1 - y_0 + 1, z_1 - z_0 + 1))

        self.anchors = []

    # Basic Getters and Setters
    def set(self, x,y,z, material):
        self._arr[int(x) - self._x_0][int(y) - self._y_0][int(z) - self._z_0] =  material

    def get(self, x, y, z):
        return self._arr[int(x) - self._x_0][int(y) - self._y_0][int(z) - self._z_0]

    def getPos0(self):
        return self._x_0, self._y_0, self._z_0

    def getPos1(self):
        return self._x_1, self._y_1, self._z_1

    # Anchors
    def setAnchor(self,x,y,z):

        if x < self._x_0 or x > self._x_1:
            return
        elif y < self._y_0 or y > self._y_1:
            return
        elif z < self._z_0 or z > self._z_1:
            return

        self.anchors.append((x,y,z))

    def getAnchor(self, i):
        return self.anchors[i]

    def alignAnchor(self, i, other, j):
        x,y,z = self.getAnchor(i)

    def getShape(self):
        return self._arr.shape

    def shift(self, dx, dy, dz):
        self._x_0 += dx
        self._y_0 += dy
        self._z_0 += dz

        self._x_1 += dx
        self._y_1 += dy
        self._z_1 += dz

    # def setRelative(self, x,y,z, material):
    #     self._arr[int(x)][int(y)][int(z)] = material

    # Resize the buffer to the given coordinates
    def resize(self, x_0, y_0, z_0, x_1, y_1, z_1):

        newArr = np.zeros((x_1 - x_0,y_1 - y_0,z_1 - z_0))

        dx_0 = self._x_0 - x_0
        dy_0 = self._y_0 - y_0
        dz_0 = self._z_0 - z_0

        for x in range(0, self._x_1 - self._x_0):
            for y in range(0, self._y_1 - self._y_0):
                for z in range(0, self._z_1 - self._z_0):
                    newArr[x + dx_0][y + dy_0][z + dz_0] = self._arr[x][y][z]

        self._arr = newArr
        self._x_0 = x_0
        self._y_0 = y_0
        self._z_0 = z_0
        self._x_1 = x_1
        self._y_1 = y_1
        self._z_1 = z_1


    def write(self, other):
        id = 0

        for x in range(self._x_0, self._x_1 + 1):
            for y in range(self._y_0, self._y_1 + 1):
                for z in range(self._z_0, self._z_1 + 1):
                    id = self.get(x,y,z)
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
    def __init__(self, mc, Zero, x_0=-10, y_0=-10, z_0=-10, x_1=10,y_1=10,z_1=10,):
        super().__init__(x_0,y_0,z_0, x_1, y_1, z_1)
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