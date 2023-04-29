import sys
import json
import os
import copy
import random
from os import path
import re

import numpy as np
from perlin_noise import PerlinNoise

from csglib.Game import Game
from csglib.primitive import *
from csglib.compound import *
from csglib.material import *

punct = r'\w+|[^\s\w]'

# !GLOBAL CONSTANTS
operators = ["Union", "Intersection", "Difference",
             "Loop","If",
             "On Ground","Shift","Rotation", "On", "North", "South", "East", "West"]
primitiveNames = ["Cube", "Sphere", "Cuboid", "Cylinder", "Pyramid", "Prism", "Cone"]
materialSelectorTypes = ["Random", "Perlin"]
reservedProperties = ["Relative"]
customShapes = []

def verify_files():
    global customShapes

    # For each file in the 'obj' directory
    for fileName in os.listdir("obj"):
        object_name = fileName.removesuffix(".json")
        customShapes.append(object_name)

# ! LANGUAGE CONSTRUCTS

def parse_program(prog):
    props = dict()

    props["Position"] = np.array([0.0, 100.0, 0.0])
    props["Orientation"] = np.identity(3)

    # Parse an expression
    return parse_expression(prog,props)

def parse_expression(prog, parent_props):
    print("Parsing expression: {}".format(prog))

    props = parse_properties(prog, parent_props)

    for key in prog:
        if key in primitiveNames:
            # print("{k} is a primitive.".format(k=key))
            return parse_primitive(prog[key],key, props)

        elif key in customShapes:
            # print("{k} is a compound.".format(k=key))
            return parse_custom_shape(prog[key], key, props)

        elif key in operators:
            # print("{k} is an operator.".format(k=key))
            return parse_operator(prog, key, props)


def parse_primitive(prog, shapeName, parent_props):
    print("Parsing Primitive:{}".format(prog))

    props = parse_properties(prog,parent_props)

    if not "Material" in prog:
        raise ValueError("Property '{p}' expected in '{s}' shape".format(p="Material",s="Primitive"))

    f = None

    if shapeName == "Cube":
        # return parse_cube(prog, props)
        f = parse_cube

    elif shapeName == "Sphere":
        # return parse_sphere(prog, props)
        f = parse_sphere

    elif shapeName == "Cylinder":
        # return parse_cylinder(prog, props)
        f = parse_cylinder

    elif shapeName == "Cuboid":
        # return parse_cuboid(prog, props)
        f = parse_cuboid

    elif shapeName == "Pyramid":
        f = parse_pyramid

    elif shapeName == "Prism":
        f = parse_prism

    elif shapeName == "Cone":
        f = parse_cone

    else:
        raise ValueError("Primitive '{}' does not exist".format(shapeName))

    return f(prog, props)    


def parse_custom_shape(prog,shapeName, parent_props):
    print("Parsing Custom Shape: {}".format(shapeName))

    props = parse_properties(prog, parent_props)

    json_path = 'obj\\'+shapeName+'.json'

    if path.exists(json_path):
        f = open(json_path)

        text = f.read()

        f.close()

        shape = json.loads(text)

        return parse_expression(shape, props)
    else:
        raise ValueError("Custom shape '{}' not found.".format(shapeName))


def parse_operator(prog, op, props):

    # 'Set' operators
    if op == "Union":
        return parse_union(prog[op], props)

    elif op == "Intersection":
        return parse_intersection(prog[op], props)

    elif op == "Difference":
        return parse_difference(prog[op],props)

    # Language Constructs
    elif op == "Loop":
        return parse_loop(prog[op], props)

    elif op == "If":
        return parse_if(prog[op],props)

    # Positional Operators
    elif op == "On Ground":
        return parse_on_ground(prog[op], props)

    elif op == "Shift":
        return parse_shift(prog[op], props)

    elif op == "Rotation":
        return parse_rotation(prog[op], props)

    elif op == "On":
        return parse_preposition_operator(prog[op], props, compound.onTopOf)

    elif op == "North":
        return parse_preposition_operator(prog[op], props, compound.northOf)

    elif op == "South":
        return parse_preposition_operator(prog[op], props, compound.southOf)

    elif op == "East":
        return parse_preposition_operator(prog[op], props, compound.eastOf)

    elif op == "West":
        return parse_preposition_operator(prog[op], props, compound.westOf)

    else:
        raise ValueError("Invalid Operator: {}".format(prog))


def parse_properties(prog, props):
    new_props = props.copy()

    for key in prog:
        if key in operators or key in primitiveNames or key in customShapes:
            continue

        # elif key == "Relative":
        #     abs_pos = new_props["Position"]
        #     orientation = new_props["Orientation"]

        #     rel_pos = parse_property(prog["Relative"], new_props)

        #     new_pos = abs_pos + np.dot(orientation,rel_pos)
        #     new_props["Position"] = new_pos
        #     continue

        else:
            new_props[key] = parse_property(prog[key], new_props)
            print("{key} -> {val}".format(key=key, val= new_props[key]))

    return new_props


def parse_property(var_expr, vars):
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
            newList.append(parse_property(item,vars))

        return newList

    # Otherwise, return literal
    else:
        return var_expr


def variable_expansion(var_exp, props):
    varName = var_exp.replace('$', '')

    return props[varName]


def function_call(fn_call, props):

    # Extract funciton name
    funName = fn_call.split('!')[1].split('(')[0]

    args_raw = fn_call.split('(', 1)[1].rsplit(')',1)[0]

    args = parse_arguments(args_raw,props)

    # print("Fun: {f}, Args:{a}".format(f=funName, a=args))

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

    elif funName == "abs":
        return abs(args[0])

    elif funName == "randInt":
        return randomInt(int(args[0]),int(args[1]))

    elif funName == "isEqual":
        return (args[0] == args[1])

    elif funName == "getBlock":
        return getBlock(args[0])

    elif funName == "rotateX":
        return rotateX(args[0], args[1])

    elif funName == "rotateY":
        return rotateY(args[0], args[1])

    elif funName == "rotateZ":
        return rotateZ(args[0], args[1])

    elif funName == "perlin":
        return perlin(args[0], args[1], args[2])

        # TODO OTHER FUNCTION CALLS
    else:
        raise ValueError("No such function is defined: {}".format(funName))


def parse_arguments(arguments, props):

    words = re.findall(punct, arguments)

    # print("Raw:{}".format(words))

    # Check that scopes are correct
    if text.count('(') > text.count(')'):
        raise ValueError("Unexpected ')' at {text}".format(text=text))

    elif text.count('(') < text.count(')'):
        raise ValueError("Expected ')' at {text}".format(text=text))

    finalArgs = []

    current_arg = ""

    i = 0
    while i < len(words):
        # print("Word:{}".format(words[i]))
        if words[i] == ",":
            finalArgs.append(current_arg)
            current_arg = ""

        elif words[i] == "(":
            # print("Forwarding to ')'")
            # Forward to close bracket

            openBracket = 0
            closeBracket = 0

            while True:
                current_arg += words[i]

                if words[i] == "(":
                    openBracket += 1

                elif words[i] == ")":
                    closeBracket += 1

                
                if openBracket == closeBracket:
                    break

                i += 1

        else:
            current_arg += words[i]

        i += 1

    finalArgs.append(current_arg)

    # print("Split:{}".format(finalArgs))
                
    args = []
    for token in finalArgs:
        value = parse_property(token, props)
        args.append(value)

    print("Evaluated:", args)

    return args


# !GEOMETRIC OPERATORS
def parse_union(prog, props):
    print("Parsing union:", prog)

    children = []
    for item in prog:
        child_node = parse_expression(item, props)
        children.append(child_node)

    return unionNode(children)


def parse_difference(prog, props):
    child_progs = []
    for item in prog:
        child_node = parse_expression(item, props)
        child_progs.append(child_node)

    return differenceNode(child_progs)


def parse_intersection(prog, props):
    inter_node = intersectionNode()

    for item in prog:
        child_node = parse_expression(item, props)
        inter_node.addChild(child_node)
    
    return inter_node

# !Language Operations
def parse_loop(prog, parent_props):

    # Checking that variables exist
    if not "Var" in prog:
        raise ValueError("No 'Var' variable in loop construct")

    elif not "Start" in prog:
        raise ValueError("No 'Start' variable in loop construct")

    elif not "End" in prog:
        raise ValueError("No 'End' variable in loop construct")

    elif not "Body" in prog:
        raise ValueError("No 'Body' variable in loop construct")

    var = prog["Var"]
    start = int(parse_property(prog["Start"], parent_props))
    end = int(parse_property(prog["End"], parent_props))

    body = prog["Body"]

    # Type checking
    if not isinstance(var, str):
        raise TypeError("Loop variable {varname} is of invalid type {type}".format(varname="Var", type = type(var)))
    
    elif not isinstance(start, int):
        raise TypeError("Loop variable {varname} is of invalid type {type}".format(varname="Start", type = type(start)))

    elif not isinstance(end, int):
        raise TypeError("Loop variable {varname} is of invalid type {type}".format(varname="End", type = type(end)))

    elif not isinstance(body, dict):
        raise TypeError("Loop variable {varname} is of invalid type {type}".format(varname="Body",type = type(body)))


    childrenProgs =[]

    for i in range(start, end):
        props = copy.copy(parent_props)
        props[var] = i

        node = parse_expression(body, props)
        childrenProgs.append(node)

    return unionNode(childrenProgs)


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
    result = parse_property(condition, parent_props)

    # Type checking result
    if not isinstance(result, bool):
        raise TypeError("Condition must have return type 'bool' and not {type}".format(type = type(result)))

    # Evaluating corresponding block
    if result:
        return parse_expression(if_block, parent_props)

    elif not else_block == None and not result:
        return parse_expression(else_block, parent_props)


# !Positional Operators
def parse_on_ground(prog, props):
    print("Parsing on ground")

    child_prog = parse_expression(prog, props)

    return onGroundNode(game, [child_prog])


def parse_preposition_operator(prog, props, f):
    print("Parsing prepostion Operator")
    if not len(prog) == 2:
        raise ValueError("Prepositional operator requires exactly {n} operands.".format(n=2))

    operands = []
    for item in prog:
        child_node = parse_expression(item, props)
        operands.append(child_node)

    return f(operands[0], operands[1])


# def parse_north(prog, props):
#     print("Parsing North")
#     if not len(prog) == 2:
#         raise ValueError("Prepositional operator requires exactly {n} operands.".format(n=2))

#     operands = []
#     for item in prog:
#         child_node = parse_expression(item, props)
#         operands.append(child_node)

#     return northNode(operands)

# def parse_on(prog, props):
#     if not len(prog) == 2:
#         raise ValueError("Prepositional operator '{o}' requires exactly {n} operands.".format(o="On", n=2))

#     operands = []
#     for item in prog:
#         child_node = parse_expression(item, props)
#         operands.append(child_node)

#     return operands[0].onTopOf(operands[1])


def parse_shift(prog, props):
    print("Parsing offset: {}".format(prog))

    if not "Offset" in prog:
        raise ValueError("No '{}' variable in loop construct".format("Offset"))

    if not "Body" in prog:
        raise ValueError("No '{}' variable in loop construct".format("Body"))

    vec = parse_property(prog["Offset"], props)
    child_prog = parse_expression(prog["Body"], props)

    if not isinstance(vec, list) or not len(vec) == 3:
        raise TypeError("{p} must be of length {l}.".format(p="Vector",l=3))


    return shiftNode(vec, [child_prog])


# def parse_north(prog, props):
#     if not len(prog) == 2:
#         raise ValueError("Prepositional operator '{o}' requires exactly {n} operands.".format(o="On", n=2))

#     operands = []
#     for item in prog:
#         child_node = parse_expression(item, props)
#         operands.append(child_node)

#     return operands[0].northOf(operands[1])
    

# def parse_north(prog, props):
#     pass


def parse_rotation(prog, props):
    if not "Axis" in prog:
        raise ValueError("{p} property expected in {o} operation".format(p="Axis", o="Rotation"))

    elif not isinstance(prog["Axis"], str):
        raise TypeError("Type {t} expected for {p} property.".format(t="String", p="Axis"))
    
    axes = ["x", "y", "z"]

    axis = axes.index(prog["Axis"].lower())

    if axis == None:
        raise ValueError("{p} property must be one of {a}".format(p="Axis", a=axes))


    if not "Degrees" in prog:
        raise ValueError("{p} property expected in {o} operation".format(p="Degrees", o="Rotation"))

    deg = parse_property(prog["Degrees"], props)

    if not isinstance(deg, (float, int)):
        raise TypeError("Type {t} expected for {p} property.".format(t="Float or Int", p="Degrees"))


    child_prog = parse_expression(prog["Body"], props)

    return rotationNode(axis, deg, [child_prog])

# !Materials
def parse_material(mat,props):
    # print("Material:",mat)

    # 'Selector' type checking
    if not "Selector" in mat:
        raise ValueError("Expected property '{p}'.".format(p="Selector"))
    
    selector = mat["Selector"]

    if not selector in materialSelectorTypes:
        raise ValueError("'{s}' is not a valid material selector".format(s=selector))


    # 'Ids' type checking
    if not "Ids" in mat:
        raise ValueError("Expected property '{p}'.".format(p="Ids"))
    
    ids = parse_property(mat["Ids"],props)


    # Random selector
    if selector == "Random":

        weights = None
        if "Weights" in mat:
            weights = parse_property(mat["Weights"],props)

        return random_material(ids, weights)


    # Perlin Noise selector
    elif selector == "Perlin":
        if "Thresholds" not in mat:
            raise ValueError("Expected property '{p}' in material with selector '{s}'.".format(p="Thresholds",s=selector))

        octaves = None
        seed = None

        if "Octaves" in mat:
            octaves = parse_property(mat["Octaves"], props)
        else:
            octaves = math.pow(2,random.randint(1,6))

        if "Seed" in mat:
            seed = parse_property(mat["Seed"], props)
        else:
            seed = random.randint(0,10000)
        

        thresholds = parse_property(mat["Thresholds"],props)

        return perlin_material(ids, thresholds, seed, octaves)

# !PRIMITIVE SHAPES
# TODO: CHECKING ARGUMENTS FOR ALL PRIMITIVES

def parse_cube(prog,props):

    size = props["Size"]
    material = parse_material(props["Material"], props)

    print("Cube(mat:{m}, size:{s}".format(m=material,s=size))

    return cube(material, size)


def parse_sphere(prog,props):

    rad = props["Radius"]
    material = parse_material(props["Material"],props)

    print("Sphere(Material:", material, ",Radius:", rad,")")

    return sphere(material, rad)


def parse_cylinder(prog, props):

    rad = props["Radius"]
    len = props["Length"]
    material = parse_material(props["Material"],props)

    print("Cylinder(mat:{material}, rad:{rad}, len{len})".format(material=material, rad=rad, len=len))

    return cylinder(material, rad, len)


def parse_cuboid(prog,props):

    material = parse_material(props["Material"],props)
    dim = props["Dimensions"]

    print("Cuboid(material:{material}, dim:{dim})".format(material=material, dim=dim))

    return cuboid(material, dim)


def parse_pyramid(prog, props):

    material = parse_material(props["Material"], props)
    height = props["Height"]
    breadth = props["Breadth"]
    width = props["Width"]

    print("Pyramid(Material:{}, Height:{}, Breadth:{}, Width:{})".format(material, height, breadth, width))
    return pyramid(material, height, breadth, width)


def parse_prism(prog, props):
    pass

def parse_cone(prog, props):
    pass

# ! ROTATING THE MATRIX
def rotateX(mat, deg):

    # Type Checking
    if not isinstance(mat, (list, np.ndarray)):
        raise TypeError("Argument 'mat' is of invalid type: {t}".format(t=type(mat)))

    elif not np.shape(mat) == (3,3):
        raise ValueError("Argument 'mat' must have dimensions '(3,3)', not {d}".format(d=np.shape(mat)))

    elif not isinstance(deg, (int,float)):
        raise TypeError("Argument 'deg' must be of types 'int' or 'float', not {t}".format(t=type(deg)))

    theta = deg* math.pi / 180

    rotation = np.array(
        [1.0,0.0,0.0,
        0.0, math.cos(theta), -math.sin(theta),
        0.0, math.sin(theta), math.cos(theta)]
    ).reshape(3,3)

    return np.matmul(mat, rotation)


def rotateY(mat, deg):

    # Type Checking
    if not isinstance(mat, (list, np.ndarray)):
        raise TypeError("Argument 'mat' is of invalid type: {t}".format(t=type(mat)))

    elif not np.shape(mat) == (3,3):
        raise ValueError("Argument 'mat' must have dimensions '(3,3)', not {d}".format(d=np.shape(mat)))

    elif not isinstance(deg, (int,float)):
        raise TypeError("Argument 'deg' must be of types 'int' or 'float', not {t}".format(t=type(deg)))

    theta = deg* math.pi / 180

    rotation = np.array(
        [math.cos(theta), 0.0, math.sin(theta),
        0.0, 1.0, 0.0,
        -math.sin(theta), 0, math.cos(theta)]
    ).reshape(3,3)

    return np.matmul(mat, rotation)


def rotateZ(mat, deg):

    # Type Checking
    if not isinstance(mat, (list, np.ndarray)):
        raise TypeError("Argument 'mat' is of invalid type: {t}".format(t=type(mat)))

    elif not np.shape(mat) == (3,3):
        raise ValueError("Argument 'mat' must have dimensions '(3,3)', not {d}".format(d=np.shape(mat)))

    elif not isinstance(deg, (int,float)):
        raise TypeError("Argument 'deg' must be of types 'int' or 'float', not {t}".format(t=type(deg)))

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

def perlin(pos, seed=random.randint(0,10000), oct=1):
    noise = PerlinNoise(seed, oct)
    pos_scaled = [1.0/(round(pos[0])+0.5), 1.0/(round(pos[1])+0.5), 1.0/(round(pos[2])+0.5)]
    noise_val = (noise.noise(pos_scaled)+1.0)/2
    print("Pos: {p},Noise Value:{v}".format(p=pos_scaled, v=noise_val))
    return noise_val

# !PARSING PROGRAM
# CHECKING FILES
verify_files()
print("Custom Shapes:", customShapes)


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

print("Finished Parsing:")
print(tree)

print("Evaluating Tree:")

pos = [50, 63, 50]
rot = np.identity(3)

buf = tree.set(pos, rot)

buf.write(game)