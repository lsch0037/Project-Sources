import math
# from vec3 import vec3
from pcglib.vec3 import vec3

class mat4():
    # Creates a new matrix of all 0s
    def __init__(self, *args):
        
        # If no arguments given, set all 0
        if len(args) == 0:
            self._arr = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

        # If an array of 16 as argument, set values to it
        elif isinstance(args[0], list) and len(args[0]) == 16:
            self._arr = args[0]

        else:
            raise TypeError("unsupported constructor type(s): '{}'").format(type(args[0]))

    # Returns the row with the given index
    def __getitem__(self,index):
        if index == 0:
            return self._arr[0:4]
        elif index == 1:
            return self._arr[4:8]
        elif index == 2:
            return self._arr[8:12]
        elif index == 3:
            return self._arr[12:16]

    def __toList__(self):
        return self._arr

    def __str__(self):
        return str(self._arr)

    def __eq__(self,other):
        if isinstance(other, mat4):
            return self._arr == other._arr

        elif isinstance(other, list):
            return self._arr == other
        
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    # Create a new matrix with the same values
    def clone(self):
        return mat4(self._arr)

    # Adding two matrices
    def __add__(self, other):
        newMat = []

        for i in range(16):
            newMat.append(self._arr[i] + other._arr[i])

        return mat4(newMat)


    # Subtracting two matrices
    def __sub__(self, other):
        newMat = []

        for i in range(16):
            newMat.append(self._arr[i] - other._arr[i])

        return mat4(newMat)


    # Perform a rotation around the X axis of theta radiants
    def rotateX(self, theta):
        result = self.clone()

        cos_term = math.cos(theta)
        sin_term = math.sin(theta)

        result._arr[4] = self._arr[4] * cos_term + self._arr[8] * sin_term
        result._arr[5] = self._arr[5] * cos_term + self._arr[9] * sin_term
        result._arr[6] = self._arr[6] * cos_term + self._arr[10] * sin_term
        result._arr[7] = self._arr[7] * cos_term + self._arr[11] * sin_term
        result._arr[8] = self._arr[8] * cos_term - self._arr[4] * sin_term
        result._arr[9] = self._arr[9] * cos_term - self._arr[5] * sin_term
        result._arr[10] = self._arr[10] * cos_term - self._arr[6] * sin_term
        result._arr[11] = self._arr[11] * cos_term - self._arr[7] * sin_term

        return result


    # Perform a rotation around the Y axis of theta radiants
    def rotateY(self,theta):
        result = self.clone()

        cos_term = math.cos(theta)
        sin_term = math.sin(theta)

        result._arr[0] = self._arr[0] * cos_term - self._arr[8] * sin_term
        result._arr[1] = self._arr[1] * cos_term - self._arr[9] * sin_term
        result._arr[2] = self._arr[2] * cos_term - self._arr[10] * sin_term
        result._arr[3] = self._arr[3] * cos_term - self._arr[11] * sin_term
        result._arr[8] = self._arr[0] * cos_term + self._arr[8] * sin_term
        result._arr[9] = self._arr[1] * cos_term + self._arr[9] * sin_term
        result._arr[10] = self._arr[2] * cos_term + self._arr[10] * sin_term
        result._arr[11] = self._arr[3] * cos_term + self._arr[11] * sin_term

        return result

    # Perform a rotation around the Z axis of theta radiants
    def rotateZ(self,theta):
        result = self.clone()

        cos_term = math.cos(theta)
        sin_term = math.sin(theta)

        result._arr[0] = self._arr[0] * cos_term + self._arr[4] * sin_term
        result._arr[1] = self._arr[1] * cos_term + self._arr[5] * sin_term
        result._arr[2] = self._arr[2] * cos_term + self._arr[6] * sin_term
        result._arr[3] = self._arr[3] * cos_term + self._arr[7] * sin_term
        result._arr[4] = self._arr[4] * cos_term - self._arr[0] * sin_term
        result._arr[5] = self._arr[5] * cos_term - self._arr[1] * sin_term
        result._arr[6] = self._arr[6] * cos_term - self._arr[2] * sin_term
        result._arr[7] = self._arr[7] * cos_term - self._arr[3] * sin_term

        return result

    # Matrix multiplication
    def __mul__(self, other):

        if isinstance(other, vec3):
            pass

        elif isinstance(other, mat4):
            result = mat4()
            for r in range(4):
                for c in range(4):

                    term1 = self._arr[c]   *other._arr[r*4] 
                    term2 = self._arr[4+c] *other._arr[r*4 + 1]
                    term3 = self._arr[8+c] *other._arr[r*4 + 2]
                    term4 = self._arr[12+c]*other._arr[r*4 + 3]
                    result._arr[r*4 + c] = term1 + term2 + term3 + term4
            
            return result
        
        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'").format(self.__class__, type(other))


    def scale(self, v):
        pass

    def translate(self, v):
        pass

    def transpose(self):
        pass

    def identity(self):
        self._arr = [1.0,0.0,0.0,0.0, 0.0,1.0,0.0,0.0, 0.0,0.0,1.0,0.0, 0.0,0.0,0.0,1.0]