import sys
import json
import os
from os import path

import numpy as np

from pcglib.vec3 import vec3
from pcglib.mat4 import mat4
from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.compound import *

# CONSTANTS
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

# CREATING GAME OBJECT
zero_offset = vec3([-144, -81, -224])
game = Game(zero_offset)

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
        # return parse_primitive(expr, props)
        return parse_shape(expr, props)
    
    # If expression is an operator
    else:
        return parse_operator(expr, props)

def parse_shape(prog, props):
    print("Parsing Shape:", prog)
    print("Props:", props)

    shape = props["Shape"]

    if shape in primitiveNames:
        return parse_primitive(prog, props, shape)

    else:
        return parse_custom_shape(prog, props, shape)

def parse_primitive(prog, props, shape):
    print("Parsing Primitive:", prog)
    print("Props:", props)

    if shape == "Cube":
        return parse_cube(prog, props)

    elif shape == "Sphere":
        return parse_sphere(prog, props)

    elif shape == "Cylinder":
        return parse_cylinder(prog, props)

    # TODO FOR OTHER SHAPES

def parse_custom_shape(prog, props, shapeName):
    print("Parsing Custom Shape")

    json_path = 'json\\'+shapeName+'.json'

    if path.exists(json_path):
        f = open(json_path)

        text = f.read()

        f.close()

        shape = json.loads(text)

        return parse_expression(shape, props)
    else:
        raise ValueError("Invalid Shape: {}".format(shapeName))

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
    material = materials[props["Material"]]
    pos = props["Position"]

    print("cube:",pos, idMat, material, size)
    print("Cube(pos:",pos,", Material:", material,"Size:",size,")")

    return cube(pos, idMat, material, size)


def parse_sphere(prog,props):
    print("Parsing Sphere:", prog)
    print("Props:", props)

    rad = props["Radius"]
    material = materials[props["Material"]]
    pos = props["Position"]

    print("Sphere(pos:",pos,", Material:", material, ",Radius:", rad,")")

    return sphere(pos, material, rad)


def parse_cylinder(prog, props):
    print("Parsing Cylinder:", prog)
    print("Props:", props)

    rad = props["Radius"]
    len = props["Length"]
    material = materials[props["Material"]]
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

def parse_props(prog, parent_props):

    props = parent_props.copy()

    for key in prog:
        if key in operatorNames:
            continue

        elif key == "Absolute" or key == "Relative":
            continue

        props[key] = parse_value(prog, props,prog[key])


    # POSITION PROPERTIES
    if "Absolute" in prog:
        props["Position"] = parse_value(prog, props, prog["Absolute"])
    
    elif "Relative" in prog:
        pos = np.array(props["Position"])
        rel = np.array(parse_value(prog, props,prog["Relative"]))
        props["Position"] = pos + rel
        print("New Position:", props["Position"])

    return props


def parse_value(prog, props, val):
    print("Parsing value:", val)
    if isinstance(val, str):
        if val[0] == '!':
            return parse_function(prog, props, val)

        elif val[0] == '$':
            return parse_variable(prog, props, val)

        else:
            return val
    
    if isinstance(val, list):
        newList = []

        for item in val:
            newList.append(parse_value(prog,props,item))

        return newList

    else:
        return val

def parse_variable(prog, props, value):
    varName = value.replace('$', '')

    print("Parsing varaible", value, "->", props[varName])

    return props[varName]

def parse_function(prog,props, value):
    print("Parsing function:", value)
    funName = value.split('!')[1].split('(')[0]
    args = value.split('(')[1].split(')')[0]

    if funName == "ground":
        return ground(args)
    

def ground(args):
    x = float(args.split(',')[0])
    z = float(args.split(',')[1])

    y = game.ground(x,z)

    return [x,y,z]


# TODO PARSE OTHER OPERATORS


tree = parse_program(prog)


tree.set(game)