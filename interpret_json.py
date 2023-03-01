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

operatorNames = ["Union", "Intersection", "Difference"]
primitiveNames = ["Cube", "Sphere", "Cuboid", "Cylinder"]

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
    props = {
        "Position" : [0.5,100.5,0.5]
    }

    # for key in prog:
    node = parse_expression(prog,props)
    tree.addChild(node)
        
    return tree

def parse_expression(expr, old_props):
    print("Parsing Expression:", expr)

    new_props = old_props.copy()

    if "Props" in prog:
        new_props = parse_props(prog["Props"], old_props)


    # If expression is a primitive
    if "Shape" in expr:
        return parse_primitive(expr, new_props)
    
    # If expression is an operator
    else:
        return parse_operator(expr, new_props)


def parse_primitive(prog, props):

    print("Parsing Primitive:", prog, ", Props:", props)
    shape = prog["Shape"]

    if shape == "Cube":
        return parse_cube(prog, props)

    elif shape == "Sphere":
        return parse_sphere(prog, props)

    elif shape == "Cylinder":
        return parse_cylinder(prog, props)

    # TODO FOR OTHER SHAPES

def parse_operator(operator, props):
    print("Parsing Operator:", prog)


    if "Union" in prog:
        return parse_union(operator["Union"], props)

    elif "Intersection" in prog:
        pass

    elif "Difference" in prog:
        pass
    # TODO FOR OTHER OPERATORS


def parse_cube(prog,props):
    print("Parsing Cube:", prog)
    size = prog["Size"]
    material = get_material(prog, props)
    pos = get_position(prog, props)

    print("cube:",pos, idMat, material, size)

    return cube(pos, idMat, material, size)


def parse_sphere(prog,props):
    print("Parsing Sphere:", prog)
    rad = prog["Radius"]
    material = get_material(prog, props)
    pos = get_position(prog, props)

    return sphere(pos, idMat, material, rad)

def parse_cylinder(prog, props):
    print("Parsing Cylinder:", prog)
    rad = prog["Radius"]
    len = prog["Length"]
    material = get_material(prog, props)
    pos = get_position(prog, props)

    return cylinder(pos, idMat, material, rad, len)


# TODO PARSE OTHER PRIMITIVES

def parse_union(prog, props):
    print("Parsing Union:", prog)
    union_node = unionNode()

    for key in prog:
        if key == "Props":
            continue

        node = parse_expression(prog[key], props)
        union_node.addChild(node)

    return union_node

def get_material(prog, props):
    mat = str()
    
    if "Material" in prog:
        mat = prog["Material"]

    else:
        mat = props["Material"]

    return materials[mat]


def get_position(prog, props):

    if "Absolute" in prog:
        pos = prog["Absolute"]
        return vec3(pos)

    elif "Relative" in prog:
        rel = prog["Relative"]
        pos = props["Position"]
        return vec3(pos) + vec3(rel)

    else:
        pos = props["Position"]
        return vec3(pos)


def parse_props(prog, props):
    print("Parsing Properties", prog)

    new_props = props.copy()

    # POSITION PROPERTIES
    if "Absolute" in prog:
        new_props["Position"] = prog["Absolute"]
    
    elif "Relative" in prog:
        new_props["Position"] = props["Position"] + prog["Relative"]

    # MATERIAL PROPERTIES
    if "Material" in prog:
        new_props["Material"] = prog["Material"]

    # print("Inner Properties:", new_props)

    return new_props


# TODO PARSE OTHER OPERATORS


tree = parse_program(prog)

zero_offset = vec3([-144, -81, -224])
game = Game(zero_offset)

tree.set(game)