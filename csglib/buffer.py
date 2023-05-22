import numpy as np
import math
import copy

class buffer():
    def __init__(self):
        self.d = dict()

    def set(self, pos, id):
        pos_x = int(pos[0])
        pos_y = int(pos[1])
        pos_z = int(pos[2])

        if pos_x not in self.d.keys():
            self.d[pos_x] = dict()

        if pos_y not in (self.d[pos_x]).keys():
            self.d[pos_x][pos_y] = dict()

        if pos_z not in ((self.d[pos_x])[pos_y]).keys():
            self.d[pos_x][pos_y][pos_z] = dict()

        self.d[pos_x][pos_y][pos_z] = id

    def get(self, pos):
        pos_x = int(pos[0])
        pos_y = int(pos[1])
        pos_z = int(pos[2])

        try:
            return self.d[pos_x][pos_y][pos_z]
        except KeyError:
            return None

    def __str__(self):
        s = ""

        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    s += "{pos}: {id}\n".format(pos=pos, id=self.get(pos))

        return s


    # REMOVES THE THE ENTRY AT THAT POSITION (UNDOES CHANGES)
    def unset(self, pos):
        pos_x = int(pos[0])
        pos_y = int(pos[1])
        pos_z = int(pos[2])

        try:
            self.d[pos_x][pos_y].pop(pos_z)
        except KeyError:
            return

    def getHeight(self, x,z):
        pos = np.array([x,255,z])

        for i in range(0,255):
            pos[1] = 255-i
            if self.get(pos) > 0:
                return 255-i
        
        return -1

    def write(self, other):
        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    other.set(pos, self.get(pos))


    def unwrite(self, other):
        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    # id1 = self.get(pos)
                    # id2 = other.get(pos)

                    # if id1 == id2:
                    other.unset(pos)


    def union(self, other):
        buf = buffer()

        self.write(buf)
        other.write(buf)

        return buf


    def difference(self,other):
        buf = copy.copy(self)

        for i in other.d:
            for j in other.d[i]:
                for k in other.d[i][j]:
                    pos = np.array([i,j,k])

                    id1 = self.get(pos)
                    id2 = other.get(pos)

                    if id1 == id2:
                        buf.unset(pos)

        return buf

    def intersection(self,other):
        newBuf = buffer()

        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    id1 = self.get(pos)
                    id2 = other.get(pos)

                    if id1 == id2:
                        newBuf.set(pos, id1)

        return newBuf