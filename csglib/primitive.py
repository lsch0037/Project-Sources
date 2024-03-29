from csglib.compound import compound
from csglib.buffer import *

import numpy as np

class primitive(compound):
    def __init__(self, material):
        self.children = []
        self.material = material


class cube(primitive):
    def __init__(self, material, size):
        super().__init__(material)
        self.size = size

    def set(self, pos, rot):
        buf = buffer()

        x_d = np.dot(rot, np.array([1,0,0]))
        y_d = np.dot(rot, np.array([0,1,0]))
        z_d = np.dot(rot, np.array([0,0,1]))

        for i in range(self.size*2):
            for j in range(self.size*2):
                for k in range(self.size*2):
                    current_pos = pos + x_d*(i/2) + y_d*(j/2) + z_d*(k/2)

                    buf.set(current_pos, self.material.get(current_pos))
        
        return buf

    # Get bounds of Cube Primitive
    def getBounds(self):
        min = np.array([0,0,0])
        max = np.array([self.size, self.size, self.size])
        
        return min, max

    def __repr__(self):
        return 'Cube'

class cuboid(primitive):
    # Constructor for a cuboid primitive
    # dim: a vector where the magnitude of i,j and k determine the dimensions of the cuboid in each direction
    def __init__(self, material, dim):
        super().__init__(material)
        self.dim = dim

    def set(self, pos, rot):
        buf = buffer()

        x_d = np.dot(rot, np.array([1,0,0]))
        y_d = np.dot(rot, np.array([0,1,0]))
        z_d = np.dot(rot, np.array([0,0,1]))

        for i in range(int(self.dim[0])*2):
            for j in range(int(self.dim[1])*2):
                for k in range(int(self.dim[2])*2):
                    current_pos = pos + x_d*(i/2) + y_d*(j/2) + z_d*(k/2)

                    buf.set(current_pos, self.material.get(current_pos))

        return buf

    # Get bounds of Cube Primitive
    def getBounds(self):
        min = np.array([0,0,0])
        max = self.dim
        
        return min, max

    def __repr__(self):
        return 'Cuboid'

class sphere(primitive):
    def __init__(self, material, rad):
        super().__init__(material)
        self.rad = rad

    def set(self,pos,rot):
        buf = buffer()

        pos0 = pos - np.array([self.rad, self.rad, self.rad])

        for x in range(int(2*self.rad)):
            for y in range(int(2*self.rad)):
                for z in range(int(2*self.rad)):
                    current_pos = pos0 + np.array([x,y,z])
                    dist = np.linalg.norm(pos - current_pos)  

                    if dist <= self.rad:
                        buf.set(current_pos, self.material.get(current_pos))
        
        return buf

    def getBounds(self):
        min = np.array([-self.rad, -self.rad, -self.rad])
        max = np.array([self.rad, self.rad, self.rad])

        return min, max

    def __repr__(self):
        return 'Sphere'

class cylinder(primitive):
    def __init__(self, material, rad, len):
        super().__init__(material)
        self.rad = rad
        self.len = len

    def set(self, pos, rot):
        buf = buffer()

        x_d = np.dot(rot, np.array([1,0,0]))
        y_d = np.dot(rot, np.array([0,1,0]))
        z_d = np.dot(rot, np.array([0,0,1]))

        for h in range(int(self.len*2)):
            center_pos = pos + y_d*(h/2)
            for i in range(int(-self.rad*2), int(self.rad*2)):
                for j in range(int(-self.rad*2), int(self.rad*2)):
                    current_pos = pos + x_d*(i/2) + y_d*(h/2) + z_d*(j/2)
                    dist = np.linalg.norm(current_pos - center_pos)  

                    if dist <= self.rad:
                        buf.set(current_pos, self.material.get(current_pos))
        
        return buf

    def getBounds(self):
        min = np.array([-self.rad, 0, -self.rad])
        max = np.array([self.rad, self.len, self.rad])

        return min, max

    def __repr__(self):
        return 'Cylinder'
        

class pyramid(primitive):
    def __init__(self, material, height, breadth, width):
        super().__init__(material)
        self.height = height
        self.breadth = breadth
        self.width = width

    def set(self, pos, rot):
        buf = buffer()

        x_d = np.dot(rot, np.array([1,0,0]))
        y_d = np.dot(rot, np.array([0,1,0]))
        z_d = np.dot(rot, np.array([0,0,1]))

        for i in range(self.height*2):
            y = i*y_d

            current_breadth = int(-(self.breadth/2 * i) / self.height + self.breadth/2)
            current_width = int(-(self.width/2 * i) / self.height + self.width/2)

            for j in range(-current_breadth*2, current_breadth*2):
                x = j*x_d*0.5

                for k in range(-current_width*2, current_width*2):
                    z = k*z_d*0.5

                    current_pos = pos + x + y + z

                    id = self.material.get(current_pos)
                    buf.set(current_pos, id)

        return buf

    def getBounds(self):
        min = np.array([-self.breadth/2, 0, -self.width/2])
        max = np.array([self.breadth/2, self.height, self.width/2])

        return min, max

    def __repr__(self):
        return 'Pyramid'


class cone(primitive):
    def __init__(self, material, height, radius):
        super().__init__(material)
        self.height = height
        self.radius = radius

    def set(self, pos, rot):
        buf = buffer()

        x_d = np.dot(rot, np.array([1,0,0]))
        y_d = np.dot(rot, np.array([0,1,0]))
        z_d = np.dot(rot, np.array([0,0,1]))

        for i in range(int(self.height)):
            y = i*y_d

            current_radius = int(-(self.radius * i) / self.height + self.radius)

            for j in range(-self.radius, self.radius):
                x = j*x_d

                for k in range(-self.radius, self.radius):
                    z = k*z_d

                    current_pos = pos + x + y + z

                    dist = np.linalg.norm(abs(x + z))

                    if dist <= current_radius:
                        id = self.material.get(current_pos)
                        buf.set(current_pos, id)

        return buf

    def getBounds(self):
        min = np.array([-self.radius, 0, -self.radius])
        max = np.array([self.radius, self.height, self.radius])

        return min, max

    def __repr__(self):
        return 'Cone'

class prism(primitive):
    pass