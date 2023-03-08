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

        searchAreaSize = max_off*2
        searchAreaPosX = center_x - max_off
        searchAreaPosZ = center_z - max_off

        bestPos = None
        minUnfitScore = float('inf')

        for x in range(searchAreaPosX, searchAreaPosX+searchAreaSize - size):
            for z in range(searchAreaPosZ, searchAreaPosZ+searchAreaSize - size):
                print("pos:",x,z)

                # dist = math.sqrt(abs(x-center_x)**2 + abs(z-center_z)**2)
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



    def write(self, other):
        print("Writing buffer...")
        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])
                    other.set(pos, self.get(pos))

        print("...Done.")