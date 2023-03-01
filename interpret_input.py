import sys
import os
from os import path
import json

# Constants
expressions = []

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


for word in splits:
    print(word)

    

def parseKnownExpression(word):

    return False