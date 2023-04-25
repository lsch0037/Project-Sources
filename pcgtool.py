import os
import sys

from input_parser import *

# * Read Arguments
if len(sys.argv) == 1:
    raise SystemError("Args must have at least length 1")

input_path = sys.argv[1]

# ! Run Input Parser
os.system("input_parser.py {}".format(input_path))

# ! Read Output Program
splits = inputPath.split("/")
fileName = splits[len(splits)-1].removesuffix(".txt")
programm_path = "Prog/{}.json".format(fileName)

os.system("language_parser.py {}".format(programm_path))

# ! Run Language Parser

# ! Evaluate CSG Tree

# ! Set Buffer to Game