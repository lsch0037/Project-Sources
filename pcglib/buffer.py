import numpy as np

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

    def ground(self, x,z):
        pos = np.array([x,255,z])

        for i in range(0,255):
            pos[1] = 255-i
            if self.get(pos) > 0:
                return 255-i
        
        return -1

    def matchSquare(self,x,z,max_off, size):
        return
        height_map = np.full((2*max_off, 2*max_off),np.empty)

        final_pos = np.array([x,height_map[x][z], z])

        # return final_pos


    def write(self, other):
        print("Writing buffer...")
        for i in self.d:
            for j in self.d[i]:
                for k in self.d[i][j]:
                    pos = np.array([i,j,k])
                    other.set(pos, self.get(pos))

        print("...Done.")