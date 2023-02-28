class buffer():
    def __init__(self):
        # self._x_offset = offset[0]
        # self._y_offset = offset[1]
        # self._z_offset = offset[2]
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

    # ? REMOVES THE THE ENTRY AT THAT POSITION (UNDOES CHANGES)
    def unset(self, pos):
        try:
            self.d[pos[0]][pos[1]].pop(pos[2])
        except KeyError:
            return

    def ground(self, x,z):
        # TODO RETURN THE HEIGHT 1 ABOVE THE GROUND ON THAT SPOT

        for i in range(0,255):
            pos = [x,255-i, z]

            if self.get(pos) > 0:
                return pos
        
        return [x, -1, z]