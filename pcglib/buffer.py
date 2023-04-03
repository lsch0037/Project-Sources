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
        # print("Set ",pos)

    def get(self, pos):
        try:
            return self.d[pos[0]][pos[1]][pos[2]]
        except KeyError:
            return -1

    # REMOVES THE THE ENTRY AT THAT POSITION (UNDOES CHANGES)
    def unset(self, pos):
        # print("Unset ", pos)
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

    def matchSquare(self,center_x,center_z,max_off, size):

        # TODO: MAKE MONTE CARLO

        # !CREATE BUFFER
        # !SET SHAPE TO BUFFER
        # !SUPERIMPOSE BUFFER ON GAME AT OFFSET 0,0
        # !GET SCORE FOR FITNESS AT POSITION
        # *IF LESS THAN THRESHOLD
            # ?MAYBE MOVE IN THE DIRECTION OF BEST FITNESS
            # ?MAYBE MOVE ONE STEP FURTHER IN ALL DIRECTIONS
            # !REPEAT

        # !ELSE STOP

        searchAreaSize = max_off*2
        searchAreaPosX = center_x - max_off
        searchAreaPosZ = center_z - max_off

        bestPos = None
        minUnfitScore = float('inf')

        for x in range(searchAreaPosX, searchAreaPosX+searchAreaSize - size):
            for z in range(searchAreaPosZ, searchAreaPosZ+searchAreaSize - size):
                print("pos:",x,z)

                dist = math.dist([x,z], [center_x, center_z])

                # print("Distance from center:", dist)

                y = self.getHeight(x,z) + 1

                blocksChanged = 0
                airUnder = 0
                for i in range(size):
                    for j in range(size):

                        if self.get([x+i, y, z+j]) != 0:
                            blocksChanged +=1

                        elif self.get([x+i, y-1, z+j]) == 0:
                            airUnder += 1

                # print("BlocksChagned:", blocksChanged)
                # print("AirUnder:", airUnder)

                unfitScore = (1+dist) * (1 + blocksChanged) * (1 + airUnder)
                # print("unfitScore:", unfitScore)

                if unfitScore < minUnfitScore:
                    minUnfitScore = unfitScore
                    bestPos = [x,y,z]

        return np.array(bestPos)


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


    def getBounds(self):
        min = np.array([np.inf, np.inf, np.inf])
        max = np.array([-np.inf, -np.inf, -np.inf])

        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    for dim in range(0,3):
                        if pos[dim] < min[dim]:
                            min[dim] = math.floor(pos[dim])

                        if pos[dim] > max[dim]:
                            max[dim] = math.ceil(pos[dim])

        mid = np.array([min[0] + (max[0] - min[0]) / 2, min[1] + (max[1] - min[1]) / 2, min[2] + (max[2] - min[2]) / 2])

        return min,mid,max


    def getTop(self):
        min,mid,max = self.getBounds()

        return np.array([mid[0], max[1], mid[2]])

    def getBottom(self):
        min,mid,max = self.getBounds()

        return np.array([mid[0], min[1], mid[2]])

    def getCenter(self):
        min, mid,max = self.getBounds()

        return mid

    def getNorth(self):
        pass

    def getSouth(self):
        pass

    def getEast(self):
        min, mid,max = self.getBounds()

        return np.array([max[0],mid[1],mid[2]])

    def getWest(self):
        pass

    def shift(self, offset):
        newBuf = buffer()

        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])

                    newBuf.set(pos + offset, self.get(pos))

        return newBuf