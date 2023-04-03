import sys
import os
from os import path
import json
import re

# TODO LOAD LIST OF DESCRIPTORS AND MODIFIERS FROM THOSE USED IN THE FILES ITSELF

objects = dict()

punct = r'\w+|[^\s\w]'

def readFile(filePath):
    f = open(filePath,"r")
    content = f.read()
    f.close()

    return json.loads(content)


def verify_files():
    global objects

    # For each file in the 'obj' directory
    for fileName in os.listdir("obj"):
        object_name = fileName.removesuffix(".json").title()
        objects[object_name] = dict()

        objPath = os.path.join('obj',fileName)
        metaPath = os.path.join('meta', fileName)

        # If that file doesn't exist
        if not os.path.isfile(objPath):
            raise ValueError("Error, file is unexpected type: {}".format(objPath))
        
        # If the corresponding meta file doesn't exist
        if not os.path.isfile(metaPath):
            raise ValueError("No metadata file for '{}'".format(fileName))

        # TODO: VERIFY THAT ALL ARGUMENTS ARE DEFINED IN META

        meta_json = readFile(metaPath)

        # If meta file doesn't have "Descriptors"
        if not "Descriptors" in meta_json:
            raise ValueError("Meta file '{f}' must have '{p}' {t} defined".format(f=metaPath, p="Descriptors", t="property"))


        # Descriptors
        if not "Default" in meta_json["Descriptors"]:
            raise ValueError("Meta file '{f}' must have '{p}' {t} defined".format(f=metaPath, p="Default", t="attribute"))

        objects[object_name]["Descriptors"] = list(meta_json["Descriptors"].keys())
        objects[object_name]["Descriptors"].remove("Default")

        # Prepositions
        objects[object_name]["Prepositions"] = list(meta_json["Modifiers"].keys())

        # TODO FOR PRLURALS

def getDescriptors(object_name):
    return objects[object_name]["Descriptors"]

def getPrepositions(object_name):
    return objects[object_name]["Prepositions"]


def tokenise(text):
    print("Tokenising paragraph: '{}'".format(text))

    words = re.findall(punct, text)

    tokens = [None] * len(words)

    for i in range(len(words)):
        current_word = words[i].title()
        # print("Word:", current_word)

        # if word is token
        if current_word in objects:
            # print(current_word, "is an object.")
            
            tokens[i] = (current_word, "Object")

        else:
            # Search forward for object
            for j in range(i+1, len(words)):
                lookahead_word = words[j].title()
                # print("Lookahead",lookahead_word)

                # if the next object has been found
                if lookahead_word in objects:
                    # print("Next object found:",lookahead_word)

                    # if the word in question is a descriptor for the next object
                    if current_word in getDescriptors(lookahead_word):
                        # print(current_word," is a descriptor of", lookahead_word)
                        tokens[i] = (current_word, "Descriptor", lookahead_word)

                    # if the word in question is a modifier for the next object
                    elif current_word in getPrepositions(lookahead_word):
                        # print(current_word," is a modifier of ", lookahead_word)
                        tokens[i] = (current_word, "Modifier", lookahead_word)

                    # TODO IF TWO WORD MODIFIER

                    # if neither
                    else:
                        # print(current_word, " has no meaning.")
                        tokens[i] = None
                    
                    # Stop looking ahead
                    break

    final_tokens = []
    for token in tokens:
        if not token == None:
            final_tokens.append(token)

    print("Tokens", final_tokens)

    return final_tokens

def parse_clause(tokens):
    obj1 = None
    obj2 = None
    modifier = None

    j = 0
    for i in range(len(tokens)):
        token = tokens[i]

        if token[1] == "Modifier":
            obj1 = parse_description(tokens[0:i])
            obj2 = parse_clause(tokens[i:])

            modifier = tokens[i]

            return eval_modifier(obj1, modifier, obj2)

    # If no modifier was found

    return parse_description(tokens)
    

# def parse_paragraph(paragraph):
#     print("Parsing paragraph: '{}'".format(paragraph))
#     sentences = paragraph.split(".")

#     if len(sentences) < 3:
#         return parse_sentence(sentences[0])

#     sentence_progs = []
#     for sentence in sentences:
#         sentence_prog = parse_sentence(sentence)
#         sentence_progs.append(sentence_prog)

#     prog = dict()

#     prog["Union"] = sentence_progs

#     return prog


# def parse_sentence(sentence):
#     print("Parsing sentence: '{}'".format(sentence))

#     clauses = sentence.split(',')

#     if len(clauses) == 1:
#         return parse_clause(clauses[0])

#     clause_progs = []
#     for clause in clauses:
#         clause_prog = parse_clause(clause)
#         clause_progs.append(clause_prog)

#     prog = dict()
#     prog["Union"] = clause_progs
#     return prog


# def parse_clause(clause):
#     print("Parsing clause: '{}'".format(clause))

#     words = clause.split()


#     for i in len(words):
#         if words[i] in objects:
#             current_description = clause.split()
#             parse_description(current_description, object_name) 
#             pass


def parse_description(tokens):
    desc = []
    objName = None

    for token in tokens:
        if token[2] == "Descriptor":
            desc.append(token)

        elif token[2] == "Object":
            objName = token[1]
        
        elif token[2] == "Modifier":
            raise ValueError("Modifier with unclear object.")
        
    prog = readFile("obj/{}.json".format(objName))
    meta = readFile("meta/{}.json".format(objName))


    # !CONTINUE HERE


def parse_clause_old(clause):
    print("Parsing clause: '{}'".format(clause))

    first_mod_index = len(clause)
    first_mod = None
    
    for m in modifiers:
        index = clause.rfind(m)
        if not index == -1 and index < first_mod_index:
            first_mod_index = index
            first_mod = m

    if first_mod == None:
        obj, desc = parse_object(clause)
        return eval_object(obj, desc)

    else:
        first_clause,mod, other_clause = clause.partition(first_mod)
        parse_clause(other_clause)
        
        print("First Obj Desc:", first_obj)
        print("Other:", other_clause)
        
        return parse_modifier(first_obj, first_mod, scnd_obj)


# Return the modifier defined on the primary object of the clause given
def parse_modifier(first_obj, modifier,second_obj):
    print("Evaluating modifier '{}'".format(modifier))

    # modifier_json = meta[second_obj]["Prepositions"][modifier]
    second_meta = meta[second_obj]
    second_mod = second_meta["Prepositions"]
    mod_json = second_mod[modifier]
    parent_props = mod_json["Parent"]
    second_props = mod_json["This"]
    first_props = mod_json["Other"]

    first_prog = parse_object(first_obj)
    for key in first_props:
        first_prog[key] = first_props[key]

    second_prog = parse_object(second_obj)
    for key in second_props:
        second_prog[key] = second_props[key]

    parent_prog = dict()
    for key in parent_props:
        parent_prog[key] = parent_props[key]

    parent_prog["Union"] = [first_prog, second_prog]
    return parent_prog


# Return the program for the object with the given descriptors
def parse_object(text):
    print("Parsing object: '{}'".format(text))
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

    return current_object, desc


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
verify_files()

print("Objects:", objects)

# Reading Input
fileName = sys.argv[1]

f = open(fileName, "r")

text = f.read()

f.close()

# TOKENISE
tokens = tokenise(text)

prog = parse_program(tokens)

# Write to 'Prog.json'
f = open('Prog.json', 'w')

f.write(json.dumps(prog, indent=4))

f.close()