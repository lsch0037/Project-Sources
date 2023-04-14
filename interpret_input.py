import sys
import os
import json
import re


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
    print("Parsing Clause: {}".format(tokens))
    obj1 = None
    obj2 = None
    modifier = None

    i = find_next_of_type(tokens,"Modifier")

    if i == -1:
        # If no modifier was found
        return parse_description(tokens)
    else:
        obj1Name, obj1 = parse_description(tokens[0:i])
        obj2Name, obj2 = parse_clause(tokens[i+1:])
        modifier = tokens[i][0]

        print("obj1:{o1}, mod:{m}, obj2:{o2}".format(o1=obj1,m=modifier,o2=obj2))


        meta2 = readFile("meta/{}.json".format(obj2Name))
        mod_name = meta2["Modifiers"][modifier]
        
        
        prog = dict()
        prog[mod_name] = [obj1, obj2]

        return obj1Name, prog
    

def find_next_of_type(tokens, type):
    for token in tokens:
        if token[1] == type:
            return tokens.index(token)
    
    return -1
    

def parse_description(tokens):
    print("Description:{}".format(tokens))
    desc = []
    objName = None

    for token in tokens:
        if token[1] == "Descriptor":
            desc.append(token[0])

        elif token[1] == "Object":
            objName = token[0]
        
        elif token[1] == "Modifier":
            raise ValueError("Modifier with unclear object.")

    print("ObjName:{}".format(objName))
    print("Desc:{}".format(desc))
        
    # obj = readFile("obj/{}.json".format(objName))
    meta = readFile("meta/{}.json".format(objName))

    prog = dict()

    prog[objName] = meta["Descriptors"]["Default"]

    for token in desc:
        desc_json = meta["Descriptors"][token]
        
        for key in desc_json:
            prog[objName][key] = desc_json[key]

    # prog[objName] = obj

    print("Prog:{}".format(prog))

    return objName, prog



# VERIFYING FILES
verify_files()


# ARGUMENTS
fileName = sys.argv[1]


# READING INPUT
f = open(fileName, "r")

text = f.read()

f.close()


# TOKENISE
tokens = tokenise(text)


# PARSE
name,prog = parse_clause(tokens)


# WRITING PROGRAM
f = open('Prog.json', 'w')

f.write(json.dumps(prog, indent=4))

f.close()