import sys
import json

from pcglib.vec3 import vec3
from pcglib.mat4 import mat4
from pcglib.Game import Game
from pcglib.primitive import cube
from pcglib.new_compound import new_compound


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
    tree = new_compound()

    print(prog)
    for key in prog:

        # Parsing Operators
        if key == "Union":
            pass
        elif key == "Intersection":
            pass
        elif key == "Difference":
            pass

        # Parsing Primitives
        elif isPrimitive(prog):
            parse_primitive(prog, tree)
        
    return tree


def isPrimitive(prog):
    if "Shape" in prog:
        return True

    return False

def parse_primitive(prog,tree):
    shape = prog["Shape"]

    if shape == "Cube":
        return parse_cube(prog, tree)

    elif shape == "Sphere":
        pass
    # TODO FOR OTHER SHAPES

def parse_cube(prog, tree):
    pos = vec3(0,100,0)
    rot = mat4()
    rot.identity()

    size = prog["Size"]
    material = prog["Material"]

    node = cube(pos, rot, material, size)
    tree.addChild(node)

tree = parse_program(prog)

zero_offset = vec3([-144, -81, -224])
game = Game(zero_offset)

tree.set(game)