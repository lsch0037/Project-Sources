class new_buffer():
    def __init__(self, offset):
        self._x_offset = offset[0]
        self._y_offset = offset[1]
        self._z_offset = offset[2]
        self.d = dict()


    def set(self, pos, id):
        if pos[0] not in self.d.keys():
            self.d[pos[0]] = dict()

        if pos[1] not in self.d[str(pos[0])].keys():
            self.d[pos[0]][pos[1]] = dict()

        if pos[2] not in self.d[pos[0]][pos[1]].keys():
            self.d[pos[0]][pos[1]][pos[2]] = dict()

        self.d[pos[0]][pos[1]][pos[2]] = id

    def get(self, pos):
        return self.d[pos[0]][pos[1]][pos[2]]
