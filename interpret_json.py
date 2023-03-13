import sys
import json
import os
import copy
from os import path

import numpy as np
import random

from pcglib.Game import Game
from pcglib.primitive import *
from pcglib.compound import *


# !GLOBAL CONSTANTS
idMat = np.identity(3)

materials = {
    "Air":0,
    "Stone": 1,
    "Wooden Planks":5,
    "Wood" : 17,
    "Leaves" : 18,
    "Diamond Block": 57
}

shapeOperators = ["Union", "Intersection", "Difference"]
primitiveNames = ["Cube", "Sphere", "Cuboid", "Cylinder"]


# ! LANGUAGE CONSTRUCTS

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

    props = variable_assign(expr, parent_props)

    # If expression is a shape
    if "Shape" in expr:
        return parse_shape(expr, props)
    
    # If expression is an operator
    else:
        return parse_operator(expr, props)


def parse_shape(prog, props):

    shape = props["Shape"]

    if shape in primitiveNames:
        return parse_primitive(prog, props, shape)

    else:
        return parse_custom_shape(prog, props, shape)


def parse_primitive(prog, props, shape):

    if shape == "Cube":
        return parse_cube(prog, props)

    elif shape == "Sphere":
        return parse_sphere(prog, props)

    elif shape == "Cylinder":
        return parse_cylinder(prog, props)

    elif shape == "Cuboid":
        return parse_cuboid(prog, props)

    # TODO FOR OTHER SHAPES


def parse_custom_shape(prog, props, shapeName):

    json_path = 'json\\'+shapeName+'.json'

    if path.exists(json_path):
        f = open(json_path)

        text = f.read()

        f.close()

        shape = json.loads(text)

        return parse_expression(shape, props)
    else:
        raise ValueError("Invalid Shape: {}".format(shapeName))


def parse_operator(prog, props):

    if "Union" in prog:
        return parse_union(prog["Union"], props)

    elif "Intersection" in prog:
        pass

    elif "Difference" in prog:
        return parse_difference(prog["Difference"],props)

    elif "Loop" in prog:
        return parse_loop(prog["Loop"], props)

    else:
        raise ValueError("Invalid Operator: {}".format(prog))


def variable_assign(json_prog, props):
    new_props = props.copy()

    for key in json_prog:
        if key == "Relative":
            abs_pos = np.array(new_props["Position"])
            rel_pos = variable_expression(json_prog["Relative"], new_props)
            new_props["Position"] = abs_pos + rel_pos
            continue

        if key in shapeOperators:
            continue

        new_props[key] = variable_expression(json_prog[key], new_props)


    return new_props


def variable_expression(var_expr, vars):
    # If the expression is a string
    if isinstance(var_expr, str):
        # If expression is a function call
        if var_expr[0] == '!':
            return function_call(var_expr, vars)

        # If expression is a variable expansion
        elif var_expr[0] == '$':
            return variable_expansion(var_expr, vars)

        # Otherwise return literal
        else:
            return var_expr
    
    # If the expression is a list
    if isinstance(var_expr, list):
        newList = []

        # For each list item, parse varaible expression
        for item in var_expr:
            newList.append(variable_expression(item,vars))

        return newList

    # Otherwise, return literal
    else:
        return var_expr


def variable_expansion(var_exp, props):
    varName = var_exp.replace('$', '')

    return props[varName]


def function_call(fn_call,props):
    funName = fn_call.split('!')[1].split('(')[0]

    args_str = fn_call.split('(')[1].split(')')[0]
    args_split = args_str.split(',')

    args = []

    for arg in args_split:
        # TODO: ALLOW FOR FUNCTION CALLS IN ARGUMENTS
        arg_cleaned = arg.replace(' ','')
        args.append(variable_expression(arg_cleaned, props))


    if funName == "getHeight":
        return getHeight(args[0], args[1])

    elif funName == "add":
        return float(args[0]) + float(args[1])

    elif funName == "sub":
        return float(args[0]) - float(args[1])

    elif funName == "mul":
        return float(args[0])*float(args[1])

    elif funName == "div":
        return float(args[0])/float(args[1])

    # elif funName == "matchSquare":
    #     return matchSquare(args[0],args[1],args[2],args[3])

    elif funName == "randInt":
        return randomInt(args[0],args[1])

        # TODO OTHER FUNCTION CALLS


# !GEOMETRIC OPERATORS
def parse_union(prog, props):
    union_node = unionNode()

    for item in prog:
        node = parse_expression(item, props)
        union_node.addChild(node)

    return union_node


def parse_difference(prog, props):
    diff_node = differenceNode()

    for item in prog:
        node = parse_expression(item, props)
        diff_node.addChild(node)

    return diff_node
    

def parse_loop(prog, parent_props):
    print("Parsing Loop")


    # Checking that variables exist
    if not "loop_var" in prog:
        raise ValueError("No 'loop_var' variable in loop construct")

    elif not "loop_range" in prog:
        raise ValueError("No 'loop_range' variable in loop construct")

    elif not "loop_body" in prog:
        raise ValueError("No 'loop_body' variable in loop construct")

    loop_var = prog["loop_var"]
    loop_range = prog["loop_range"]
    body = prog["loop_body"]


    # Type checking
    if not isinstance(loop_var, str):
        raise TypeError("Loop variable 'loop_var' is of invalid type {type}".format(varname=loop_var, type = type(loop_var)))
    
    elif not isinstance(loop_range, int):
        raise TypeError("Loop variable 'loop_start' is of invalid type {type}".format(varname=loop_start, type = type(loop_var)))

    elif not isinstance(body, dict):
        raise TypeError("Loop variable {varname} is of invalid type {type}".format(type = type(loop_var)))

    uNode = unionNode()

    for i in range(0, loop_range):
        props = copy.copy(parent_props)
        props[loop_var] = i

        node = parse_expression(body, props)
        uNode.addChild(node)

    return uNode


    
# !PRIMITIVE SHAPES
def parse_cube(prog,parent_props):
    props = variable_assign(prog,parent_props)

    size = props["Size"]
    material = materials[props["Material"]]
    pos = props["Position"]

    print("Cube(pos:",pos,", Material:", material,"Size:",size,")")

    return cube(pos, idMat, material, size)


def parse_sphere(prog,props):

    rad = props["Radius"]
    material = materials[props["Material"]]
    pos = props["Position"]

    print("Sphere(pos:",pos,", Material:", material, ",Radius:", rad,")")

    return sphere(pos, material, rad)


def parse_cylinder(prog, props):

    rad = props["Radius"]
    len = props["Length"]
    material = materials[props["Material"]]
    pos = props["Position"]

    print("Cylinder(pos:{pos}, rot:{rot}, mat:{material}, rad:{rad}, len{len})".format(pos=pos, rot=idMat, material=material, rad=rad, len=len))

    return cylinder(pos, idMat, material, rad, len)


def parse_cuboid(prog,props):

    pos = props["Position"]
    rot = idMat
    material = materials[props["Material"]]
    dim = props["Dimensions"]

    print("Cuboid(pos:{pos}, rot:{rot}, material:{material}, dim:{dim})".format(pos=pos, rot=rot, material=material, dim=dim))

    return cuboid(pos, idMat, material, dim)


# !BUILT IN FUNCTIONS
def getHeight(x, z):
    return game.getHeight(float(x),float(z))


def matchSquare(x,z,max_offset, size):
    return game.matchSquare(x,z,max_offset, size)


def randomInt(min, max):
    return random.randint(min, max)


# !PARSING PROGRAM
# INTERPRETING ARGUMENT
fileName = sys.argv[1]

# READING FILE
f = open(fileName, "r")

text = f.read()

f.close()

# CREATING GAME OBJECT
zero_offset = np.array([-144, -81, -224])
game = Game(zero_offset)

# CREATING JSON OBJECT
prog = json.loads(text)

tree = parse_program(prog)

print("Finished")

tree.set(game)