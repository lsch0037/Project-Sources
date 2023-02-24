import sys
import json

from pcglib.vec3 import vec3
from pcglib.mat4 import mat4
from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.compound import *

# CONSTANTS
origin = vec3(0.5,100.5,0.5)
idMat = mat4()
idMat.identity()

materials = {
    "Air":0,
    "Stone": 1,
    "Wood" : 17,
    "Leaves" : 18
}

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
    print("Parsing Program:", prog)
    tree = compound()

    # for key in prog:
    node = parse_expression(prog)
    tree.addChild(node)
        
    return tree

def parse_expression(prog):
    print("Parsing Expression:", prog)
    if "Shape" in prog:
        return parse_primitive(prog)
    
    else:
        return parse_operator(prog)


def parse_primitive(prog):
    print("Parsing Primitive:", prog)
    shape = prog["Shape"]

    if shape == "Cube":
        return parse_cube(prog)

    elif shape == "Sphere":
        return parse_sphere(prog)

    elif shape == "Cylinder":
        return parse_cylinder(prog)

    # TODO FOR OTHER SHAPES

def parse_operator(prog):
    print("Parsing Operator:", prog)
    if "Union" in prog:
        return parse_union(prog["Union"])

    elif "Intersection" in prog:
        pass

    elif "Difference" in prog:
        pass
    # TODO FOR OTHER OPERATORS


def parse_cube(prog):
    print("Parsing Cube:", prog)
    size = prog["Size"]
    material = prog["Material"]

    return cube(origin, idMat, material, size)


def parse_sphere(prog):
    print("Parsing Sphere:", prog)
    rad = prog["Radius"]
    material = get_material(prog)

    return sphere(origin, idMat, material, rad)

def parse_cylinder(prog):
    print("Parsing Cylinder:", prog)
    rad = prog["Radius"]
    len = prog["Length"]
    material = get_material(prog)

    return cylinder(origin, idMat, material, rad, len)


# TODO PARSE OTHER PRIMITIVES

def parse_union(prog):
    print("Parsing Union:", prog)
    union_node = unionNode()

    for key in prog:
        node = parse_expression(prog[key])
        union_node.addChild(node)
        print("Added expression to node")

    return union_node

def get_material(prog):
    if not "Material" in prog:
        return 0

    mat = prog["Material"]

    if isinstance(mat, int):
        return mat

    elif isinstance(mat, str):
        if mat not in materials:
            raise ValueError("Material '",mat,"' is not defined")
            # return None
        else:
            return materials[mat]

    elif isinstance(mat, dict):
        # ? IF MATERIAL EXPRESSION
        pass


# TODO PARSE OTHER OPERATORS


tree = parse_program(prog)

zero_offset = vec3([-144, -81, -224])
game = Game(zero_offset)

tree.set(game)