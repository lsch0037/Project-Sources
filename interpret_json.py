import sys
import json

import numpy as np

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
    tree = compound()
    props = {
        "Position" : [0.5, 100.5, 0.5]
    }

    # Parse an expression
    node = parse_expression(prog,props)
    tree.addChild(node)
        
    return tree

def parse_expression(expr, parent_props):

    print("Parsing Expression:", expr)
    props = parse_props(expr, parent_props)
    print("Props:", props)

    # If expression is a primitive
    if "Shape" in expr:
        return parse_primitive(expr, props)
    
    # If expression is an operator
    else:
        return parse_operator(expr, props)


def parse_primitive(prog, props):

    print("Parsing Primitive:", prog)
    print("Props:", props)
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


def parse_cube(prog,parent_props):
    props = parse_props(prog,parent_props)
    print("Parsing Cube:", prog)
    print("Props:", props)

    size = props["Size"]
    material = props["Material"]
    pos = props["Position"]

    print("cube:",pos, idMat, material, size)
    print("Cube(pos:",pos,", Material:", material,"Size:",size,")")

    return cube(pos, idMat, material, size)


def parse_sphere(prog,props):
    print("Parsing Sphere:", prog)
    print("Props:", props)

    rad = props["Radius"]
    material = props["Material"]
    pos = props["Position"]

    print("Sphere(pos:",pos,", Material:", material, ",Radius:", rad,")")

    return sphere(pos, material, rad)


def parse_cylinder(prog, props):
    print("Parsing Cylinder:", prog)
    rad = props["Radius"]
    len = props["Length"]
    material = props["Material"]
    pos = props["Position"]

    return cylinder(pos, idMat, material, rad, len)


# TODO PARSE OTHER PRIMITIVES

def parse_union(prog, props):
    print("Parsing Union:", prog)
    union_node = unionNode()

    for item in prog:
        node = parse_expression(item, props)
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
        return np.array(pos)

    elif "Relative" in prog:
        rel = np.array(prog["Relative"])
        pos = np.array(props["Position"])
        return np.add(pos,rel)

    else:
        pos = props["Position"]
        return np.array(pos)


def parse_props(prog, parent_props):

    props = parent_props.copy()

    for key in prog:
        if key in operatorNames:
            continue

        elif key == "Absolute" or key == "Relative":
            continue

        props[key] = prog[key]


    # POSITION PROPERTIES
    if "Absolute" in prog:
        props["Position"] = prog["Absolute"]
    
    elif "Relative" in prog:
        pos = np.array(props["Position"])
        rel = np.array(prog["Relative"])
        props["Position"] = pos + rel

    return props

def parse_variable(prog, props):
    pass

def parse_function(prog,props):
    pass


# TODO PARSE OTHER OPERATORS


tree = parse_program(prog)

# zero_offset = vec3([-144, -81, -224])
# game = Game(zero_offset)

# tree.set(game)