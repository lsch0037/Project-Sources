import sys
import os
from os import path
import json

# !Importing nlp library
import spacy

nlp = spacy.load("en_core_web_sm")

descriptors = ["Big", "Small", "Large", "Tall", "Short"]
modifiers = ["on","on top of", "next to", "under"]

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
    

# def parse_literal(token, expected):
#     if token == expected:
#         return
#     else:
#         raise ValueError("Expected literal:{}".format(expected))


# def parse_verb(token):

#     if token in verbs:
#         return token
#     else:
#         return None


# def parse_noun(tokens, ctr):
#     pathName = 'json\\'+tokens[ctr]+'.json'
    
#     if path.exists(pathName):
#         ctr += 1
#         return json.loads(pathName)
#     else:
#         raise ValueError("No such file : '{}'".format(pathName))


# def parse_sentence(tokens, ctr):
#     parse_literal(tokens[0], "A")

#     verb = parse_verb(tokens[1])

#     noun = parse_noun(tokens, ctr)
#     parse_literal('.', tokens, ctr)

#     return createObject(noun,verb)

def tokensise(text):
    tokens = []

    sentences = text.split(".")
    for sentence in sentences:

        phrases = sentence.split(",")
        phrase_tkns = []
        for phrase in phrases:

            words = phrase.split()
            phrase_tkns.append(words)
        
        tokens.append(phrase_tkns)

    return tokens


def parse_paragraph(paragraph):
    sentences = paragraph.split('.')

    sentence_progs = []
    for sentence in sentences:
        sentence_prog = parse_sentence(sentence)
        sentence_progs.append(sentence_prog)
    

    prog = dict()

    prog["Union"] = sentence_progs

    return prog

def parse_sentence(sentence):
    # doc = nlp(sentence)
    # obj_type = None
    # obj_attrs = []
    
    # for token in doc:
    #     tkn_text = token.text.title()
    #     if tkn_text in objects:
    #         obj_type = tkn_text
    #     elif tkn_text in verbs:
    #         obj_attrs.append(tkn_text)

    # print("Objects:", obj_type)
    # print("Attributes:",obj_attrs)

    # prog = eval_object(obj_type, obj_attrs)

    # return prog

    clauses = sentence.split(',')

    clause_progs = []
    for clause in clauses:
        clause_prog = parse_clause(clause)
        clause_progs.append(clause_prog)

    prog = dict()
    prog["Union"] = clause_progs
    return prog

def parse_clause(clause):
    words = clause.split()

    obj_description = []

    for i in range(len(words)):
        if words[i] in modifiers:
            # TODO parse 2 word modifiers like "next to"
            pass

        else:
            obj_description.append(words[i])

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
# tokens = tokensise(text)
# print("Tokens:", tokens)

# prog = parse_sentence(text)
prog = parse_paragraph(text)

# Write to 'Prog.json'
f = open('Prog.json', 'w')

f.write(json.dumps(prog, indent=4))

f.close()