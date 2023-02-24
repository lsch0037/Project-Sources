import sys
import json

from pcglib.vec3 import vec3
from pcglib.mat4 import mat4
from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.compound import compound

# CONSTANTS
origin = vec3(0.5,100.5,0.5)
idMat = mat4()
idMat.identity()


# INTERPRETING ARGUMENT
fileName = sys.argv[1]

# READING FILE
f = open(fileName, "r")

text = f.read()

f.close()

# print(text)

# CREATING JSON OBJECT
prog = json.loads(text)

def parse_program(prog):
    tree = compound()

    for key in prog:

        # Parsing Operators
        if key == "Union":
            subTree = parse_union(prog)
            tree.addChild(subTree)

        elif key == "Intersection":
            pass

        elif key == "Difference":
            pass

        # Parsing Primitives
        elif isPrimitive(prog):
            node = parse_primitive(prog)
            tree.addChild(node)
        
    return tree


def isPrimitive(prog):
    if "Shape" in prog:
        return True

    return False


def parse_primitive(prog):
    shape = prog["Shape"]

    if shape == "Cube":
        return parse_cube(prog)

    elif shape == "Sphere":
        return parse_sphere(prog)

    # TODO FOR OTHER SHAPES

def parse_cube(prog):
    size = prog["Size"]
    material = prog["Material"]

    return cube(origin, idMat, material, size)


def parse_sphere(prog):
    rad = prog["Radius"]
    material = prog["Material"]

    return sphere(origin, idMat, material, rad)

# TODO PARSE OTHER PRIMITIVES

def parse_union(prog):
    return None

# TODO PARSE OTHER OPERATORS


tree = parse_program(prog)

zero_offset = vec3([-144, -81, -224])
game = Game(zero_offset)

tree.set(game)