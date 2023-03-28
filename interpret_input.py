import sys
import os
from os import path
import json

# !Importing nlp library
# import spacy

# nlp = spacy.load("en_core_web_sm")

descriptors = ["Big", "Small", "Large", "Tall", "Short"]
modifiers = ["on", "on top of", "next to", "under", "in", "south of", "north of", "east of", "west of"]

objects = dict()
meta = dict()

def check_files():
    global objects
    global meta

    for objName in os.listdir("obj"):
        objPath = os.path.join('obj',objName)
        metaPath = os.path.join('meta', objName)

        if not os.path.isfile(objPath):
            raise ValueError("Error, file is unexpected type: {}".format(objPath))
        
        if not os.path.isfile(metaPath):
            raise ValueError("No metadata file for '{}'".format(objName))

        f = open(objPath,"r")
        objText = f.read()
        f.close()

        f = open(metaPath,"r")
        metaText = f.read()
        f.close()

        objJson = json.loads(objText)
        metaJson = json.loads(metaText)

        objNameCleaned = objName.removesuffix(".json")

        objects[objNameCleaned] = objJson
        meta[objNameCleaned] = metaJson
    
# def tokensise(text):
#     tokens = []

#     sentences = text.split(".")
#     for sentence in sentences:

#         phrases = sentence.split(",")
#         phrase_tkns = []
#         for phrase in phrases:

#             words = phrase.split()
#             phrase_tkns.append(words)
        
#         tokens.append(phrase_tkns)

#     return tokens


def parse_paragraph(paragraph):
    print("Parsing paragraph: '{}'".format(paragraph))
    sentences = paragraph.split(".")
    print("Sentences:",sentences)

    if len(sentences) < 3:
        return parse_sentence(sentences[0])

    sentence_progs = []
    for sentence in sentences:
        sentence_prog = parse_sentence(sentence)
        sentence_progs.append(sentence_prog)

    prog = dict()

    prog["Union"] = sentence_progs

    return prog

def parse_sentence(sentence):
    print("Parsing sentence: '{}'".format(sentence))

    clauses = sentence.split(',')

    if len(clauses) == 1:
        return parse_clause(clauses[0])

    clause_progs = []
    for clause in clauses:
        clause_prog = parse_clause(clause)
        clause_progs.append(clause_prog)

    prog = dict()
    prog["Union"] = clause_progs
    return prog


def parse_clause(clause):
    print("Parsing clause: '{}'".format(clause))

    first_mod_index = len(clause)
    first_mod = None
    
    for m in modifiers:
        index = clause.rfind(m)
        if not index == -1 and index < first_mod_index:
            first_mod_index = index
            first_mod = m

    if first_mod == None:
        return parse_object(clause)

    else:
        # print("Evaluating modifier '{}'".format(first_mod))
        # splits = clause.split(first_mod, 1)
        first_clause, mod, second_clause = clause.partition(first_mod)
        
        first_obj = parse_object(first_clause)
        mod = parse_modifier(second_clause, first_mod)
        second_obj = parse_clause(second_clause)

        return eval_modifier(first_obj, mod, second_obj)

# Return the modifier defined on the primary object of the clause given
def parse_modifier(clause, modifier):
    print("Evaluating modifier '{}'".format(modifier))
    words = clause.split()

    obj = None

    for word in words:
        if word in objects:
            obj = word

    return meta[obj]["Modifiers"][modifier]


# Return the program for the object with the given descriptors
def parse_object(text):
    words = text.split()

    desc = []
    current_object = None
    for word in words:
        if word.lower() in descriptors:
            desc.append(word.lower())

        elif word.title() in objects:
            current_object = word.title()
            break

    if current_object == None:
        raise ValueError("Object description '{}' does not contain an object type.".format(text))

    return eval_object(current_object, desc)

def eval_attributes(object_name, object_attributes):
    meta_attributes = meta[object_name]["Attributes"]
    props = meta_attributes["Default"]

    for attrib in object_attributes:
        if attrib not in meta_attributes:
            raise ValueError("'{a}' is not a valid descriptor for '{o}' object".format(a=attrib,o=object_name))
        
        current_attribute = meta_attributes[attrib]

        for key in current_attribute:
            props[key] = current_attribute[key]

    return props


def eval_object(object_name, object_attributes):

    props = eval_attributes(object_name, object_attributes)
    obj_prog = objects[object_name]

    prog = dict()

    for key in props:
        prog[key] = props[key]
    
    for key in obj_prog:
        prog[key] = obj_prog[key]

    print("Final Program:", prog)
    return prog


# Checking Files
check_files()

# print("Obj: {}".format(objects))
# print("Meta: {}".format(meta))

# Reading Input
fileName = sys.argv[1]

f = open(fileName, "r")

text = f.read()

f.close()

# TOKENISE
prog = parse_paragraph(text)

# Write to 'Prog.json'
f = open('Prog.json', 'w')

f.write(json.dumps(prog, indent=4))

f.close()