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
materials = {
    "Air":0,
    "Stone": 1,
    "Grass":2,
    "Dirt":3,
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
    props = dict()

    props["Position"] = np.array([0.0, 100.0, 0.0])
    props["Orientation"] = np.identity(3)

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

    elif "If" in prog:
        return parse_if(prog["If"],props)

    else:
        raise ValueError("Invalid Operator: {}".format(prog))


def variable_assign(json_prog, props):
    new_props = props.copy()

    for key in json_prog:
        if isinstance(json_prog[key], dict):
            continue

        elif key == "Relative":
            abs_pos = new_props["Position"]
            orientation = new_props["Orientation"]

            rel_pos = variable_expression(json_prog["Relative"], new_props)

            new_pos = abs_pos + np.dot(orientation,rel_pos)
            print("New Position: {n}".format(n=new_pos))
            new_props["Position"] = new_pos
            continue

        elif key in shapeOperators:
            continue

        new_props[key] = variable_expression(json_prog[key], new_props)
        print("{key} -> {val}".format(key=key, val= new_props[key]))

    return new_props


def variable_expression(var_expr, vars):
    # print("Variable Expression:", var_expr)
    # If the expression is a string
    if isinstance(var_expr, str):
        # If expression is a function call
        if var_expr[0] == '!':
            return function_call(var_expr, vars)

        # If expression is a variable expansion
        elif var_expr[0] == '$':
            return variable_expansion(var_expr, vars)

        # If expression is a string of a number
        elif var_expr.replace(".","").replace("-","").isnumeric():
            return float(var_expr)

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

    # Extract funciton name
    funName = fn_call.split('!')[1].split('(')[0]

    args_raw = fn_call.split('(', 1)[1].rsplit(')',1)[0]

    args = parse_arguments(args_raw,props)

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

    elif funName == "pow":
        return math.pow(args[0],args[1])

    elif funName == "sqrt":
        return math.sqrt(args[0])

    elif funName == "randInt":
        return randomInt(int(args[0]),int(args[1]))

    elif funName == "isEqual":
        return (args[0] == args[1])

    elif funName == "getBlock":
        return getBlock(args[0])

    elif funName == "rotateX":
        return rotateX(args[0], args[1])
        # TODO OTHER FUNCTION CALLS
    else:
        raise ValueError("No such function is defined: {}".format(funName))


def parse_arguments(arguments, props):
    print("Arguments:",arguments)

    # Replace all spaces
    text = arguments.replace(' ','')

    # Check that scopes are correct
    if text.count('(') > text.count(')'):
        raise ValueError("Unexpected ')' at {text}".format(text=text))

    elif text.count('(') < text.count(')'):
        raise ValueError("Expected ')' at {text}".format(text=text))


    splits = text.split(',')

    print("splits:", splits)
    tokens = []

    i = 0
    while i < len(splits):
        token = splits[i]

        if token[0] == '!' and token.find(')') == -1:
            
            j = i + 1
            while splits[j].find(')') == -1:
                token += splits[j]
                j += 1
            else:
                target_token = splits[j]

                token = token + ','+ target_token.split(')')[0] + ')'

                i = j
        
        tokens.append(token)
        i += 1

    print("Tokens:", tokens)
                
    args = []
    for token in tokens:
        value = variable_expression(token, props)
        args.append(value)

    print("Final evaluated arguments:", args)

    return args


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
        raise TypeError("Loop variable {varname} is of invalid type {type}".format(varname="loop_var", type = type(loop_var)))
    
    elif not isinstance(loop_range, int):
        raise TypeError("Loop variable {varname} is of invalid type {type}".format(varname="loop_range", type = type(loop_range)))

    elif not isinstance(body, dict):
        raise TypeError("Loop variable {varname} is of invalid type {type}".format(varname="loop_body",type = type(body)))

    uNode = unionNode()

    for i in range(0, loop_range):
        props = copy.copy(parent_props)
        props[loop_var] = i

        node = parse_expression(body, props)
        uNode.addChild(node)

    return uNode


def parse_if(prog, parent_props):

    if not "if_condition" in prog:
        raise ValueError("No 'if_condition' variable in 'if' construct")

    elif not "if_block" in prog:
        raise ValueError("No 'if_block' variable in 'if' construct")
    

    condition = prog["if_condition"]
    if_block = prog["if_block"]

    else_block = None

    if "else_block" in prog:
        else_block = prog["else_block"]



    # Type checking
    if not isinstance(condition, (str, bool)):
        raise TypeError("If variable {varname} is of invalid type {type}".format(varname="if_condition", type = type(condition)))
    
    elif not isinstance(if_block, dict):
        raise TypeError("If variable {varname} is of invalid type {type}".format(varname="if_block", type = type(if_block)))

    if not else_block == None and not isinstance(else_block, dict):
        raise TypeError("If variable {varname} is of invalid type {type}".format(varname="else_block", type = type(else_block)))


    # Evaluating condition
    result = variable_expression(condition, parent_props)

    # Type checking result
    if not isinstance(result, bool):
        raise TypeError("Condition must have return type 'bool' and not {type}".format(type = type(result)))

    # Evaluating corresponding block
    if result:
        return parse_expression(if_block, parent_props)

    elif not else_block == None and not result:
        return parse_expression(else_block, parent_props)

    
# !PRIMITIVE SHAPES
def parse_cube(prog,parent_props):
    props = variable_assign(prog,parent_props)

    size = props["Size"]
    material = materials[props["Material"]]
    pos = props["Position"]
    orientation = props["Orientation"]
    print(type(orientation))

    print("Cube(pos:{p}, rot:{r}, mat:{m}, size:{s}".format(p=pos,r=orientation,m=material,s=size))

    return cube(pos, orientation, material, size)


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
    orientation = props["Orientation"]

    print("Cylinder(pos:{pos}, rot:{rot}, mat:{material}, rad:{rad}, len{len})".format(pos=pos, rot=orientation, material=material, rad=rad, len=len))

    return cylinder(pos, orientation, material, rad, len)


def parse_cuboid(prog,props):

    pos = props["Position"]
    orientation = props["Orientation"]
    material = materials[props["Material"]]
    dim = props["Dimensions"]

    print("Cuboid(pos:{pos}, rot:{rot}, material:{material}, dim:{dim})".format(pos=pos, rot=orientation, material=material, dim=dim))

    return cuboid(pos, orientation, material, dim)

# ! ROTATING THE MATRIX
def rotateX(mat, deg):

    # Type Checking
    if not isinstance(mat, (list, np.ndarray)):
        raise TypeError("Argument 'mat' is of invalid type: {t}".format(t=type(mat)))

    elif not np.shape(mat) == (3,3):
        raise ValueError("Argument 'mat' must have dimensions '(3,3)', not {d}".format(d=np.shape(mat)))

    elif not isinstance(deg, (int,float)):
        raise TypeError("Argument 'deg' must be of types 'int' or 'float', not {t}".format(t=type(deg)))

    # np_map = np.array(mat).reshape(3,3)
    # print(np_map)

    theta = deg* math.pi / 180

    rotation = np.array(
        [1.0,0.0,0.0,
        0.0, math.cos(theta), -math.sin(theta),
        0.0, math.sin(theta), math.cos(theta)]
    ).reshape(3,3)

    return np.matmul(mat, rotation)

def rotateY(mat, deg):
    theta = float(deg)* math.pi / 180.0

    rotation = np.array(
        [math.cos(theta), 0.0, math.sin(theta),
        0.0, 1.0, 0.0,
        -math.sin(theta), 0, math.cos(theta)]
    ).reshape(3,3)

    return np.matmul(mat, rotation)

def rotateZ(mat, deg):
    theta = deg* math.pi / 180

    rotation = np.array(
        [math.cos(theta), -math.sin(theta), 0.0,
        math.sin(theta), math.cos(theta), 0.0,
        0.0, 0.0, 1.0]
    ).reshape(3,3)

    return np.matmul(mat, rotation)

# !BUILT IN FUNCTIONS
def getHeight(x, z):
    return game.getHeight(float(x),float(z))


def matchSquare(x,z,max_offset, size):
    return game.matchSquare(x,z,max_offset, size)


def randomInt(min, max):
    return random.randint(min, max)

def getBlock(pos):
    return game.get(pos)


# !PARSING PROGRAM
# INTERPRETING ARGUMENT
fileName = sys.argv[1]

# READING FILE
f = open(fileName, "r")

text = f.read()

f.close()

# CREATING GAME OBJECT
zero_pc = np.array([-144, -81, -224])
zero_laptop = np.array([-95.0, -65.0, -63.0])

game = Game(zero_pc)

# CREATING JSON OBJECT
prog = json.loads(text)

tree = parse_program(prog)

print("Finished")

tree.set(game)