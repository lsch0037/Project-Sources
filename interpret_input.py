import sys
import os
from os import path
import json

def loadJson(file):
    f = open(file,"r")

    text = f.read()

    f.close()

    return json.loads(text)

# Reading Input
fileName = sys.argv[1]

f = open(fileName, "r")

text = f.read()

f.close()

# Split text into words
splits = text.split()

# If there is no 'json' folder, create it
if not path.isdir('json'):
    print("Could not find 'json' folder, created it.")
    os.mkdir('json')

# Parse words
prog = dict()

for word in splits:
    json_path = 'json\\'+word+'.json'
    
    if path.exists(json_path):
        print("Parsing expression:", word)

        expr = loadJson(json_path)

        prog[word] = expr

    else:
        print("No known expression:",word)

print(prog)

# Write to 'Prog.json'
f = open('Prog.json', 'w')

f.write(json.dumps(prog, indent=4))

f.close()