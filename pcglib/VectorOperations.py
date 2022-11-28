import numpy as np

class Vector():
    def __init__(self, arr):
        self._arr = np.array(arr)

    def get(self, index):
        return self._arr[index]

    def toList(self):
        return self._arr.tolist()

    def __add__(self, vec2):
        return Vector(np.add(self._arr, vec2._arr))

    def __sub__(self, vec2):
        return Vector(np.subtract(self._arr, vec2._arr))

    def __mul__(self, vec2):
        return Vector(np.cross(self._arr, vec2._arr))

    def __truediv__(self, scalar:int):
        return Vector(np.divide(self._arr, scalar))
        
    #Returns the absolute distance of the vector
    def getLenght(self):
        return np.linalg.norm(self._arr)

    def getDirection(self):
        len = self.getLenght()
        return Vector(self._arr / len)

    def transform(self, transform):
        # TODO: IMPLEMENT 
        return -1