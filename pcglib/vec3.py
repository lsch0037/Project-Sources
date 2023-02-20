import math

class vec3():
    def __init__(self, x,y,z):
        self._arr = [x,y,z]

    def __getitem__(self, index):
        return self._arr[index]

    def toList(self):
        return self._arr

    def __str__(self):
        return "["+ str(self._arr[0]) +", "+ str(self._arr[1]) +", "+ str(self._arr[2])+ "]"

    def __eq__(self, other):
        if isinstance(other, vec3):
            return self._arr == other._arr

        elif isinstance(other, list):
            return self._arr == other
        
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))


    def __add__(self, other):
        if isinstance(other, vec3):
            return vec3(self._arr[0] + other._arr[0],self._arr[1] + other._arr[1],self._arr[2] + other._arr[2])

        elif isinstance(other, list):
            return vec3(self._arr[0] + other[0] ,self._arr[1] + other[1], self._arr[2] + other[2])

        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))


    def __sub__(self, other):
        if isinstance(other, vec3):
            return vec3(self._arr[0] - other._arr[0],self._arr[1] - other._arr[1],self._arr[2] - other._arr[2])

        elif isinstance(other, list):
            return vec3(self._arr[0] - other[0] ,self._arr[1] - other[1], self._arr[2] - other[2])

        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'").format(self.__class__, type(other))
        

    #Returns the absolute distance of the vector
    def __abs__(self):
        return math.sqrt(self._arr[0]**2 + self._arr[1]**2 + self._arr[2]**2)

    def __mul__(self, other):
        # TODO DO CROSS MULTIPLICATION
        pass

    # Divides each value in the vector by the scalar
    def __truediv__(self, scalar):
        # Check if scalar is zero
        if scalar == 0:
            raise ValueError("Cannot Divide by 0")

        # Scalar division
        elif isinstance(scalar, (int, float)):
            return vec3(self._arr[0]/scalar, self._arr[1]/scalar, self._arr[2]/scalar)

        else:
            raise TypeError("unsupported operand type(s) for /: '{}' and '{}'").format(self.__class__, type(scalar))
        
    # Returns the direction vector
    def dir(self):
        return self / abs(self)