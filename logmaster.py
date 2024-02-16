def printInfo(msg):
    print("[\033[34m*\033[0m] " + msg)
def printWarning(msg):
    print("[\033[33m!\033[0m] " + msg)
def printError(msg, exitcode):
    print("[\033[31mX\033[0m] " + msg)
    exit(exitcode)