import numpy as np
import math

class buffer():
    def __init__(self):
        self.d = dict()

    def set(self, pos, id):
        if pos[0] not in self.d.keys():
            self.d[pos[0]] = dict()

        if pos[1] not in (self.d[pos[0]]).keys():
            self.d[pos[0]][pos[1]] = dict()

        if pos[2] not in ((self.d[pos[0]])[pos[1]]).keys():
            self.d[pos[0]][pos[1]][pos[2]] = dict()

        self.d[pos[0]][pos[1]][pos[2]] = id

    def get(self, pos):
        try:
            return self.d[pos[0]][pos[1]][pos[2]]
        except KeyError:
            return -1

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
        try:
            self.d[pos[0]][pos[1]].pop(pos[2])
        except KeyError:
            return

    def getHeight(self, x,z):
        pos = np.array([x,255,z])

        for i in range(0,255):
            pos[1] = 255-i
            if self.get(pos) > 0:
                return 255-i
        
        return -1

    def write(self, other, offset=np.array([0,0,0])):
        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    other.set(pos + offset, self.get(pos))


    def unwrite(self, other, offset=np.array([0,0,0])):
        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    id1 = self.get(pos)
                    id2 = other.get(pos)

                    if id1 == id2:
                        other.unset(pos)

    def union(self, other, offset=np.array([0,0,0])):
        buf = buffer()

        self.write(buf)
        other.write(buf)

        return buf


    def difference(self,other, offset=np.array([0,0,0])):
        buf = buffer()

        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    id1 = self.get(pos)
                    id2 = other.get(pos)

                    if not id1 == id2:
                        other.set(pos)

        return buf

    def intersection(self,other, offset=np.array([0,0,0])):
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


    # def getBounds(self):
    #     min = np.array([np.inf, np.inf, np.inf])
    #     max = np.array([-np.inf, -np.inf, -np.inf])


    #     for i in self.d:
    #         for j in self.d[i]:
    #             for k in self.d[i][j]:
    #                 pos = np.array([i,j,k])

    #                 for dim in range(0,3):
    #                     if pos[dim] < min[dim]:
    #                         min[dim] = math.floor(pos[dim])

    #                     if pos[dim] > max[dim]:
    #                         max[dim] = math.ceil(pos[dim])

    #     # print("Bounds - Max:{x}, Min:{n}".format(x=max, n=min))

    #     mid = np.array([min[0] + (max[0] - min[0]) / 2, min[1] + (max[1] - min[1]) / 2, min[2] + (max[2] - min[2]) / 2])

    #     return min,mid,max


    # def getTop(self):
    #     min,mid,max = self.getBounds()

    #     return np.array([mid[0], max[1], mid[2]])

    # def getBottom(self):
    #     min,mid,max = self.getBounds()

    #     return np.array([mid[0], min[1], mid[2]])

    # def getCenter(self):
    #     min,mid,max = self.getBounds()

    #     return mid

    # def getEast(self):
    #     min,mid,max = self.getBounds()

    #     return np.array([max[0],mid[1],mid[2]])

    # def getSouth(self):
    #     min,mid,max = self.getBounds()

    #     return np.array([mid[0],mid[1],max[2]])

    # def getWest(self):
    #     min,mid,max = self.getBounds()

    #     return np.array([min[0],mid[1],mid[2]])

    # def getNorth(self):
    #     min, mid,max = self.getBounds()

    #     return np.array([mid[0],mid[1],min[2]])

    def shift(self, offset):
        newBuf = buffer()

        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    newBuf.set(pos + offset, self.get(pos))

        self.d = newBuf.d