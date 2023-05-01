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
            return parse_primitive(prog[key],key, props)

        elif key in customShapes:
            return parse_custom_shape(prog[key], key, props)

        elif key in operators:
            return parse_operator(prog, key, props)


def parse_primitive(prog, shapeName, parent_props):
    print("Parsing Primitive:{}".format(prog))

    props = parse_properties(prog,parent_props)

    material_raw = expectAttribute("Material", prog, props, dict)
    material = parse_material(material_raw, props)

    f = None

    if shapeName == "Cube":
        f = parse_cube

    elif shapeName == "Sphere":
        f = parse_sphere

    elif shapeName == "Cylinder":
        f = parse_cylinder

    elif shapeName == "Cuboid":
        f = parse_cuboid

    elif shapeName == "Pyramid":
        f = parse_pyramid

    elif shapeName == "Prism":
        f = parse_prism

    elif shapeName == "Cone":
        f = parse_cone

    else:
        raise ValueError("Primitive '{}' does not exist".format(shapeName))

    return f(prog, props, material)    


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

    
    # Prepositional Operators
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


# TODO: REPLACE EACH INSTANCE OF THIS FUNCTION WITH PARSING INDIVIDUALLY THE PROPERTIES
def parse_properties(prog, props):
    new_props = props.copy()

    for key in prog:
        if key in operators or key in primitiveNames or key in customShapes:
            continue

        else:
            new_props[key] = parse_property(prog[key], new_props)
            print("{key} -> {val}".format(key=key, val= new_props[key]))

    return new_props


def parse_property(var_expr, props):
    # If the expression is a string
    if isinstance(var_expr, str):
        # If expression is a function call
        if var_expr[0] == '!':
            return function_call(var_expr, props)

        # If expression is a variable expansion
        elif var_expr[0] == '$':
            varName = var_expr.replace('$', '')
            return props[varName]

        # If expression is a string of a number
        elif var_expr.replace(".","").replace("-","").isnumeric():
            # TODO: ALLOW FOR - SYMBOL, MAKE NEGATIVE
            return float(var_expr)

        # Otherwise return literal
        else:
            return var_expr
    
    # If the expression is a list
    if isinstance(var_expr, list):
        newList = []

        # For each list item, parse varaible expression
        for item in var_expr:
            newList.append(parse_property(item,props))

        return newList

    # Otherwise, return literal
    else:
        return var_expr


def function_call(fn_call, props):

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

    elif funName == "abs":
        return abs(args[0])

    elif funName == "randInt":
        return randomInt(int(args[0]),int(args[1]))

    # Boolean funcitons
    elif funName == "isEqual":
        return (args[0] == args[1])

    elif funName == "less":
        pass

    elif funName == "greater":
        pass

    elif funName == "getBlock":
        return getBlock(args[0])

    elif funName == "perlin":
        return perlin(args[0], args[1], args[2])

        # TODO OTHER FUNCTION CALLS
    else:
        raise ValueError("No such function is defined: {}".format(funName))


def parse_arguments(arguments, props):

    words = re.findall(punct, arguments)

    # Check that scopes are correct
    if text.count('(') > text.count(')'):
        raise ValueError("Unexpected ')' at {text}".format(text=text))

    elif text.count('(') < text.count(')'):
        raise ValueError("Expected ')' at {text}".format(text=text))

    finalArgs = []

    current_arg = ""

    i = 0
    while i < len(words):
        if words[i] == ",":
            finalArgs.append(current_arg)
            current_arg = ""

        elif words[i] == "(":
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

                
    args = []
    for token in finalArgs:
        value = parse_property(token, props)
        args.append(value)

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
def expectAttribute(attr_name, prog, props, attr_types=None):
    if not attr_name in prog:
        raise ValueError("Attribute '{}' expected in scope '{}'".format(attr_name, prog))

    val = parse_property(prog[attr_name], props)
    
    if not isinstance(val, attr_types):
        raise ValueError("Value of '{}' in scope '{}' expected to be of type(s) '{}' instead of '{}'".format(attr_name, prog, attr_types, type(val)))

    return val


def parse_loop(prog, parent_props):
    print("Parsing Loop: '{}'".format(prog))

    var = expectAttribute("Var", prog, parent_props, str)
    start = int(expectAttribute("Start", prog, parent_props, (int, float)))
    end = int(expectAttribute("End", prog, parent_props, (int, float)))
    body = expectAttribute("Body", prog, parent_props, dict)

    childrenProgs =[]

    for i in range(start, end):
        props = copy.copy(parent_props)
        props[var] = i

        node = parse_expression(body, props)
        childrenProgs.append(node)

    return unionNode(childrenProgs)


def parse_if(prog, props):
    print("Parsing If: '{}'".format(prog))

    condition = expectAttribute("Condition", prog, props, bool)
    body = expectAttribute("Body", prog, props, dict)
    
    if condition:
        return parse_expression(body, props)

    else:
        return compound([])


# !Positional Operators
def parse_on_ground(prog, props):
    print("Parsing on ground:'{}'".format(prog))

    child_prog = parse_expression(prog, props)

    return onGroundNode(game, [child_prog])


def parse_preposition_operator(prog, props, f):
    print("Parsing prepostion Operator: {}".format(prog))
    if not len(prog) == 2:
        raise ValueError("Prepositional operator requires exactly {n} operands.".format(n=2))

    operands = []
    for item in prog:
        child_node = parse_expression(item, props)
        operands.append(child_node)

    return f(operands[0], operands[1])



def parse_shift(prog, props):
    print("Parsing Shift: {}".format(prog))

    offset = expectAttribute("Offset", prog, props, list)
    body = expectAttribute("Body", prog, props, dict)

    if not len(offset) == 3:
        raise TypeError("{p} must be of length {l}.".format(p="Vector",l=3))

    body_prog = parse_expression(body, props)

    return shiftNode(offset, [body_prog])


def parse_rotation(prog, props):
    print("Parsing Rotation: '{}'".format(prog))

    axis_raw = expectAttribute("Axis", prog, props, str)
    deg = expectAttribute("Degrees", prog, props, (float, int))
    body = expectAttribute("Body", prog, props, dict)
    
    axes = ["x", "y", "z"]

    axis = axes.index(axis_raw.lower())

    if axis == None:
        raise ValueError("{p} property must be one of {a}".format(p="Axis", a=axes))

    body_prog = parse_expression(body, props)

    return rotationNode(axis, deg, [body_prog])

# !Materials
def parse_material(prog,props):
    print("Parsing Material:",prog)

    selector = expectAttribute("Selector", prog, props, str)
    ids = expectAttribute("Ids", prog, props, list)

    if not selector in materialSelectorTypes:
        raise ValueError("'{s}' is not a valid material selector".format(s=selector))


    # Random selector
    if selector == "Random":

        weights = None
        if "Weights" in prog:
            weights = parse_property(prog["Weights"],props)

        return random_material(ids, weights)


    # Perlin Noise selector
    elif selector == "Perlin":
        thresholds = expectAttribute("Thresholds", prog, props, list)

        octaves = None
        seed = None

        if "Octaves" in prog:
            octaves = parse_property(prog["Octaves"], props)
        else:
            octaves = math.pow(2,random.randint(1,6))

        if "Seed" in prog:
            seed = parse_property(prog["Seed"], props)
        else:
            seed = random.randint(0,10000)
        
        return perlin_material(ids, thresholds, seed, octaves)

# !PRIMITIVE SHAPES

def parse_cube(prog, props, material):

    size = expectAttribute("Size", prog, props, (int, float))

    print("Cube(mat:{m}, size:{s})".format(m=material,s=size))
    return cube(material, size)


def parse_sphere(prog, props, material):

    rad = expectAttribute("Radius", prog, props, (int, float))

    print("Sphere(Material:", material, ",Radius:", rad,")")
    return sphere(material, rad)


def parse_cylinder(prog, props, material):

    rad = expectAttribute("Radius", prog, props, (int, float))
    length = expectAttribute("Length", prog, props, (int, float))

    print("Cylinder(mat:{material}, rad:{rad}, len:{len})".format(material=material, rad=rad, len=length))
    return cylinder(material, rad, length)


def parse_cuboid(prog,props, material):

    dim = expectAttribute("Dimensions", prog, props, list)

    if not len(dim) == 3:
        raise ValueError("'Dimensions' attribute must be of length 3: {}".format(dim))

    print("Cuboid(material:{material}, dim:{dim})".format(material=material, dim=dim))
    return cuboid(material, dim)


def parse_pyramid(prog, props, material):

    height = expectAttribute("Height", prog, props, (int, float))
    breadth = expectAttribute("Breadth", prog, props, (int, float))
    width = expectAttribute("Width", prog, props, (int, float))

    print("Pyramid(Material:{}, Height:{}, Breadth:{}, Width:{})".format(material, height, breadth, width))
    return pyramid(material, height, breadth, width)


def parse_prism(prog, props, material):
    pass

def parse_cone(prog, props, material):

    height = expectAttribute("Height", prog, props, (int, float))
    radius = expectAttribute("Radius", prog, props, (int, float))

    print("Cone(Material:{}, Height:{}, Radius:{})".format(material, height, radius))
    return cone(material, height, radius)


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