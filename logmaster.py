from colormaster import set_color
def printInfo(msg: str):
    print(f"[{set_color('blue')}*{set_color(0)}] " + msg)


def printWarning(msg: str):
    print(f"[{set_color('yellow')}!{set_color(0)}] " + msg)


def printError(msg: str, exitcode: int):
    print(f"[{set_color('red')}X{set_color(0)}] " + msg)
    exit(exitcode)
