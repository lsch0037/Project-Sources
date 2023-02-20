import math

class mat4():
    # Creates a new identity matrix
    def __init__(self, *args):
        
        if len(args) == 0:
            self._arr = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]

        elif isinstance(args[0], list) and len(args[0]) == 16:
            self._arr = args[0]

        else:
            raise TypeError("unsupported constructor type(s): '{}'").format(type(args[0]))

    def __getitem__(self,index):
        return self._arr[index]

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



    def rotateY(self,theta):
        result = self.clone()

        cos_term = math.cos(theta)
        sin_term = math.sin(theta)

        self._arr[2] = self._arr[2] * cos_term - self._arr[10] * sin_term
        self._arr[3] = self._arr[3] * cos_term - self._arr[11] * sin_term
        self._arr[8] = self._arr[0] * cos_term + self._arr[8] * sin_term
        self._arr[9] = self._arr[1] * cos_term + self._arr[9] * sin_term
        self._arr[10] = self._arr[2] * cos_term + self._arr[10] * sin_term
        self._arr[11] = self._arr[3] * cos_term + self._arr[11] * sin_term

        return result

    def rotateZ(self):
        pass
        

    # Matrix multiplication
    def __mul__(self, other):
        pass

    def scale(self, v):
        pass

    def translate(self, v):
        pass

    def transpose(self):
        pass

    def identity(self):
        pass