import numpy as np

class boundingBox():
    def __init__(self):
        self.min = None
        self.max = None

    def calculate(self,buf):
        min = np.array([np.inf, np.inf, np.inf])
        max = np.array([-np.inf, -np.inf, -np.inf])

        for i in buf.d:
            for j in buf.d[i]:
                for k in buf.d[i][j]:
                    pos = np.array([i,j,k])

                    for dim in range(0,3):
                        if pos[dim] < min[dim]:
                            min[dim] = pos[dim]

                        if pos[dim] > max[dim]:
                            max[dim] = pos[dim]

        self.min = min
        self.max = max

    def __str__(self) -> str:
        return "Min:{min}, Max:{max}".format(min=self.min, max = self.max)


    def combine(self, boxes):
        min, max = np.array([[np.inf, np.inf, np.inf]]), np.array([-np.inf, -np.inf, -np.inf])

        for box in boxes:
            for dim in range(0,3):
                if box[dim] < min[dim]:
                    min[dim] = box[dim]

                if box[dim] > max[dim]:
                    max[dim] = box[dim]
                

        self.min = min
        self.max = max

    
    def on(self):
        x = self.max[0] - self.min[0] / 2
        z = self.max[2] - self.min[2] / 2

        return np.array([x,self.max[1], z])


    def inside(self):
        x = self.max[0] - self.min[0] / 2
        y = self.max[1] - self.min[1] / 2
        z = self.max[2] - self.min[2] / 2

        return np.array([x,y,z])

    def east(self):
        y = self.max[1] - self.min[1] / 2
        z = self.max[2] - self.min[2] / 2

        return np.array([self.max[0], y,z])

    def west(self):
        y = self.max[1] - self.min[1] / 2
        z = self.max[2] - self.min[2] / 2

        return np.array([self.min[0], y,z])

    def south(self):
        x = self.max[0] - self.min[0] / 2
        y = self.max[1] - self.min[1] / 2

        return np.array(x,y,self.max[2])

    def north(self):
        x = self.max[0] - self.min[0] / 2
        y = self.max[1] - self.min[1] / 2

        return np.array(x,y,self.min[2])

