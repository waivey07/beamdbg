import sys
import logmaster as log

if len(sys.argv) != 4:
    log.printError(f"Usage: {sys.argv[0]} <code file> <input file> <output file>", 1)

code_file = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

try:
    log.printInfo(f"reading code file \"{code_file}\"...")
    with open(code_file, "r") as f:
        code = f.read()
    log.printInfo(f"successfully readed code file \"{code_file}\"")
except FileNotFoundError:
    log.printError(f"Cannot found code file \"{code_file}\"", 2)

try:
    log.printInfo(f"reading input file \"{input_file}\"...")
    with open(input_file, "r") as f:
        inp = f.read()
    log.printInfo(f"successfully readed input file \"{input_file}\"")
except FileNotFoundError:
    log.printError(f"Cannot found input file \"{input_file}\"", 3)

output_fp = open(output_file, "w")
