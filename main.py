import sys
import logmaster as log
import help

version = "0.0.1"
log.printInfo("Beamdbg v" + version)
if len(sys.argv) != 4:
    log.printError(f"Usage: {sys.argv[0]} <code file> <input file> <output file>", 1)

code_file = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

output_fp = open(output_file, "w")


def show_code(x=None, y=None):
    if x == None and y == None:
        print(code)
    else:
        print(code[y][x])
        return code[y][x]


RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3


class Process:
    def __init__(self, code, input, height, width):
        self.index_x = 0
        self.index_y = 0
        self.current_direction = RIGHT
        self.beam = 0
        self.store = 0
        self.memory = [0 for _ in range(256)]
        self.code = code
        self.input = input
        self.input_idx = 0
        self.height = height
        self.width = width
        self.halted = False
        self.reason = ""
        self.output = ""

    def interpret(self, c):
        if self.halted:
            return self.reason
        if c == ">":
            self.current_direction = RIGHT
        elif c == "<":
            self.current_direction = LEFT
        elif c == "^":
            self.current_direction = UP
        elif c == "v":
            self.current_direction = DOWN
        elif c == "+":
            self.beam += 1
        elif c == "-":
            self.beam -= 1
        elif c == "@":
            # sys.stdout.write(chr(self.beam))
            print("Received output :", chr(self.beam))
            output_fp.write(chr(self.beam))
            self.output += chr(self.beam)
        elif c == ":":
            # sys.stdout.write(str(self.beam))
            print("Received output :", str(self.beam))
            output_fp.write(str(self.beam))
            self.output += str(self.beam)
        elif c == "/":
            if self.current_direction == RIGHT:
                self.current_direction = UP
            elif self.current_direction == LEFT:
                self.current_direction = DOWN
            elif self.current_direction == UP:
                self.current_direction = RIGHT
            elif self.current_direction == DOWN:
                self.current_direction = LEFT
        elif c == "\\":
            if self.current_direction == RIGHT:
                self.current_direction = DOWN
            elif self.current_direction == LEFT:
                self.current_direction = UP
            elif self.current_direction == UP:
                self.current_direction = LEFT
            elif self.current_direction == DOWN:
                self.current_direction = RIGHT
        elif c == "!":
            if self.beam != 0:
                if self.current_direction == RIGHT:
                    self.current_direction = LEFT
                elif self.current_direction == LEFT:
                    self.current_direction = RIGHT
                elif self.current_direction == UP:
                    self.current_direction = DOWN
                elif self.current_direction == DOWN:
                    self.current_direction = UP
        elif c == "?":
            if self.beam == 0:
                if self.current_direction == RIGHT:
                    self.current_direction = LEFT
                elif self.current_direction == LEFT:
                    self.current_direction = RIGHT
                elif self.current_direction == UP:
                    self.current_direction = DOWN
                elif self.current_direction == DOWN:
                    self.current_direction = UP
        elif c == "|":
            if self.current_direction == RIGHT:
                self.current_direction = LEFT
            elif self.current_direction == LEFT:
                self.current_direction = RIGHT
        elif c == "_":
            if self.current_direction == UP:
                self.current_direction = DOWN
            elif self.current_direction == DOWN:
                self.current_direction = UP
        elif c == "H":
            self.halted = True
            self.reason = "OK"
            print("Output :", self.output)
        elif c == "S":
            self.store = self.beam
        elif c == "L":
            self.beam = self.store
        elif c == "s":
            self.memory[self.beam] = self.store
        elif c == "g":
            self.store = self.memory[self.beam]
        elif c == "P":
            self.memory[self.store] = self.beam
        elif c == "p":
            self.beam = self.memory[self.store]
        elif c == "u":
            if self.beam != self.store:
                self.current_direction = UP
        elif c == "n":
            if self.beam != self.store:
                self.current_direction = DOWN
        elif c == "`":
            self.store -= 1
        elif c == "'":
            self.store += 1
        elif c == ")":
            if self.store != 0:
                self.current_direction = LEFT
        elif c == "(":
            if self.store != 0:
                self.current_direction = RIGHT
        elif c == "r":
            self.beam = self.input[self.input_idx]
            self.input_idx += 1

    def ni(self, count):
        for i in range(count):
            if self.halted:
                return self.reason
            print(self.index_x, self.index_y)
            self.interpret(self.code[self.index_y][self.index_x])
            if self.current_direction == RIGHT:
                self.index_x += 1
                if self.index_x >= self.width:
                    self.halted = True
                    print("Output :", self.output)
                    self.reason = "Beam was out of range"
            elif self.current_direction == LEFT:
                self.index_x -= 1
                if self.index_x < 0:
                    self.halted = True
                    print("Output :", self.output)
                    self.reason = "Beam was out of range"
            elif self.current_direction == UP:
                self.index_y -= 1
                if self.index_y < 0:
                    self.halted = True
                    print("Output :", self.output)
                    self.reason = "Beam was out of range"
            elif self.current_direction == DOWN:
                self.index_y += 1
                if self.index_y >= self.height:
                    self.halted = True
                    print("Output :", self.output)
                    self.reason = "Beam was out of range"


prefix = "beamdbg> "
log.printInfo('For help, type "help".')
p = None

while True:
    cmd = input(prefix)
    if cmd == "":
        cmd = prev
    else:
        prev = cmd
    cmd = cmd.split(" ")
    if len(cmd) > 1:
        param = cmd[1:]
    else:
        param = None
    cmd = cmd[0]
    if cmd == "help":
        print(help.help_msg)
    elif cmd == "b":
        continue
    elif cmd == "ni":
        if not p:
            log.printWarning("Process not found")
            continue
        if not param:
            p.ni(1)
        else:
            try:
                p.ni(int(param[0]))
            except ValueError:
                log.printWarning("ValueError")
                log.printWarning("Usage: ni <int>")
                continue
    elif cmd == "start":
        print()
        log.printInfo("Starting to debug...")
        readable_chars = "><^v+-@:/\\!?|_HSLsgPpun`')(r\n "
        try:
            log.printInfo(f"Loading code file \033[34m{code_file}\033[0m...")
            with open(code_file, "r") as f:
                code = f.read()
            log.printInfo(f"Code file successfully loaded \033[34m{code_file}\033[0m")
        except FileNotFoundError:
            log.printError(f"Code file not found \033[34m{code_file}\033[0m", 2)

        try:
            log.printInfo(f"Loading input file \033[32m{input_file}\033[0m...")
            with open(input_file, "r") as f:
                inp = f.read()
            log.printInfo(f"Input file successfully loaded \033[32m{input_file}\033[0m")
        except FileNotFoundError:
            log.printError(f"Cannot found input file \033[32m{input_file}\033[0m", 3)
            for c in code:
                if c not in readable_chars:
                    log.printWarning(
                        f"Found unreadable char \033[31m{c}\033[0m in code, it will be ignored."
                    )
        splitted_code = code.split("\n")
        height = len(splitted_code)
        width = max([len(l) for l in splitted_code])
        log.printInfo(f"Code height: {height}")
        log.printInfo(f"Code width: {width}")
        p = Process(splitted_code, inp, height, width)
        print()
    elif cmd == "run":
        continue
    elif cmd == "exit" or cmd == "quit":
        exit(0)
    else:
        log.printInfo('Unknown command. type "help" for help.')
