import sys

def errorHandler(msg, exitcode):
    print(msg)
    exit(exitcode)
if len(sys.argv) != 4:
    errorHandler(f"Usage: {sys.argv[0]} <code file> <input file> <output file>", 1)
