import numpy as np

class Vector():
    def __init__(self, arr):
        self._arr = np.array(arr)

    def __getitem__(self, index):
        return self._arr[index]

    def toList(self):
        return self._arr.tolist()

    def __str__(self):
        return "["+ str(self._arr[0]) +", "+ str(self._arr[1]) +", "+ str(self._arr[2])+ "]"

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self._arr == other.__arr

        elif isinstance(other, list):
            return self._arr == other
        
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))


    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(np.add(self._arr, other._arr))

        elif isinstance(other, list):
            return Vector(np.add(self._arr, other))

        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __sub__(self, other):
        return Vector(np.subtract(self._arr, other._arr))

    def __mul__(self, other):
        return Vector(np.cross(self._arr, other._arr))

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