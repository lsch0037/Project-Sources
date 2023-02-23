import math

class vec3():
    def __init__(self, *args):
        if len(args) == 0:
            self._arr = [0,0,0]
        
        elif len(args) == 1 and isinstance(args[0], list):
            self._arr = args[0]

        elif len(args) == 3:
            self._arr = [args[0], args[1], args[2]]

        else:
            raise TypeError("unsupported constructor type(s): '{}'").format(type(args[0]))

    def __getitem__(self, index):
        return self._arr[index]

    def toList(self):
        return self._arr

    def __str__(self):
        return str(self._arr)

    def __eq__(self, other):
        if isinstance(other, vec3):
            return self._arr == other._arr

        elif isinstance(other, list):
            return self._arr == other
        
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))


    # Adding two vectors
    def __add__(self, other):

        result = vec3()

        if isinstance(other, vec3):

            for i in range(3):
                result._arr[i] = self._arr[i] + other._arr[i]

        elif isinstance(other, list):
            for i in range(3):
                result._arr[i] = self._arr[i] + other[i]

        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

        return result


    # Subtracting two vectors
    def __sub__(self, other):
        result = []
        otherArray = []

        if isinstance(other, vec3):
            otherArray = other._arr

        elif isinstance(other, list):
            otherArray = other

        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'").format(self.__class__, type(other))

        for i in range(3):
            result.append(self._arr[i] - otherArray[i])

        return vec3(result)
        

    #Returns the absolute distance of the vector
    def __abs__(self):
        return math.sqrt(self._arr[0]**2 + self._arr[1]**2 + self._arr[2]**2)

    # Cross multiplication of two vectors
    def __mul__(self, other):
        result = vec3()

        # if other is a scalar
        if isinstance(other, (int, float)):

            for i in range(3):
                result._arr[i] = self._arr[i] * other


        # If other is vector, cross multiplication
        elif isinstance(other, vec3):
            result._arr[0] = self._arr[1]*other._arr[2] - self._arr[2]*other._arr[1]
            result._arr[1] = -self._arr[0]*other._arr[2] + self._arr[2]*other._arr[0]
            result._arr[2] = self._arr[0]*other._arr[1] - self._arr[1]*other._arr[0]
            

        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'").format(self.__class__, type(other))

        return result

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

    # Create a new vector with the same values
    def clone(self):
        return vec3(self._arr[0], self._arr[1], self._arr[2])
        
    # Returns the direction vector
    def dir(self):
        return self / abs(self)