import os
import sys

# * Read Arguments
if len(sys.argv) == 1:
    raise SystemError("Args must have at least length 1")

input_path = sys.argv[1]

splits = input_path.split("/")
fileName = splits[len(splits)-1].removesuffix(".txt")
outputPath = "Prog/{}.json".format(fileName)

print(outputPath)

# ! Run Input Parser
os.system("input_parser.py {} {}".format(input_path, outputPath))

# ! Read Output Program

os.system("language_parser.py {}".format(outputPath))

# ! Run Language Parser

# ! Evaluate CSG Tree

# ! Set Buffer to Game