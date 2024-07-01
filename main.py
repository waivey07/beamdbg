#!/usr/bin/env python3

import sys
import modules.logmaster as log
import modules.help as help
from modules.colormaster import set_color

version = "24.07.01"
log.printInfo("Beamdbg v" + version)
if len(sys.argv) != 4:
    log.printError(f"Usage: {sys.argv[0]} <code file> <input file> <output file>", 1)

code_file = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]


def show_code(x=None, y=None):
    if x == None and y == None:
        print(code)
    else:
        for i in range(len(splitted_code)):
            for j in range(len(splitted_code[i])):
                if i == y and j == x:
                    print(
                        f"{set_color('red', isBackground = 1)}{splitted_code[i][j]}{set_color(0)}",
                        end="",
                    )
                else:
                    print(f"{splitted_code[i][j]}", end="")
            print()


def check_ascii(c):
    return c >= 0x20 and c <= 0x7F


def show_memory(modified_memory_index, memory, beam, store):
    for i in modified_memory_index:
        if int(i) == store and int(i) == beam:
            if check_ascii(memory[i]):
                character = (
                    f"{set_color('yellow',isBright=1)}{chr(memory[i])}{set_color(0)}"
                )
                print(
                    f"Memory[{i}] {set_color('magenta', isBright=1, isBackground = 1)}(Beam){set_color(0)} {set_color('cyan', isBright=1, isBackground = 1)}(Store){set_color(0)} : {memory[i]}   <{character}>"
                )
            else:
                print(
                    f"Memory[{i}] {set_color('magenta', isBright=1, isBackground = 1)}(Beam){set_color(0)} {set_color('cyan', isBright=1, isBackground = 1)}(Store){set_color(0)} : {memory[i]}"
                )
            continue
        elif int(i) == beam:
            if check_ascii(memory[i]):
                character = (
                    f"{set_color('yellow',isBright=1)}{chr(memory[i])}{set_color(0)}"
                )
                print(
                    f"Memory[{i}] {set_color('magenta', isBright=1, isBackground = 1)}(Beam){set_color(0)} : {memory[i]}   <{character}>"
                )
            else:
                print(
                    f"Memory[{i}] {set_color('magenta', isBright=1, isBackground = 1)}(Beam){set_color(0)} : {memory[i]}"
                )

            continue
        elif int(i) == store:
            if check_ascii(memory[i]):
                character = (
                    f"{set_color('yellow',isBright=1)}{chr(memory[i])}{set_color(0)}"
                )
                print(
                    f"Memory[{i}] {set_color('cyan', isBright=1, isBackground = 1)}(Store){set_color(0)} : {memory[i]}   <{character}>"
                )
            else:
                print(
                    f"Memory[{i}] {set_color('cyan', isBright=1, isBackground = 1)}(Store){set_color(0)} : {memory[i]}"
                )
            continue
        else:
            if check_ascii(memory[i]):
                character = (
                    f"{set_color('yellow',isBright=1)}{chr(memory[i])}{set_color(0)}"
                )
                print(f"Memory[{i}] : {memory[i]}   <{character}>")
            else:
                print(f"Memory[{i}] : {memory[i]}")
            continue


RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3


class Process:
    def __init__(self, code, input, height, width):
        self.breakpoint = []
        self.modified_memory_index = []
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
        self.interrupted = False

    def show_status(self):
        show_code(self.index_x, self.index_y)
        print(f"Current index : {self.index_x}, {self.index_y}")
        if check_ascii(self.beam):
            character = (
                f"{set_color('yellow',isBright=1)}{chr(self.beam)}{set_color(0)}"
            )
            print(f"Current value of 'Beam' : {self.beam}   <{character}>")
        else:
            print(f"Current value of 'Beam' : {self.beam}")
        if check_ascii(self.store):
            character = (
                f"{set_color('yellow',isBright=1)}{chr(self.store)}{set_color(0)}"
            )
            print(f"Current value of 'Store' : {self.store}   <{character}>")
        else:
            print(f"Current value of 'Store' : {self.store}")

    def interpret(self, c):
        if self.halted:
            return self.reason

        # show_code(self.index_x, self.index_y)
        # print(f"Current index : {p.index_x}, {p.index_y}")
        # print(f"Current value of 'Beam' : {p.beam}")
        # print(f"Current value of 'Store' : {p.store}")
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
            log.printInfo(f"Received output : {chr(self.beam)}")
            output_fp = open(output_file, "a")
            output_fp.write(chr(self.beam))
            output_fp.close()
            self.output += chr(self.beam)
        elif c == ":":
            log.printInfo(f"Received output : {str(self.beam)}")
            output_fp = open(output_file, "a")
            output_fp.write(str(self.beam))
            output_fp.close()
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
            self.beam = ord(self.input[self.input_idx])
            if self.beam == 10:
                self.beam = 0
            self.input_idx += 1
        for i in range(256):
            if self.memory[i] != 0:
                self.modified_memory_index.append(i)
        self.modified_memory_index = list(sorted(set(self.modified_memory_index)))
    def run(self, count = None):
        self.interrupted = False
        if not count:
            while True:
                for i in range(len(self.breakpoint)):
                    if self.breakpoint[i][0] == self.index_x and self.breakpoint[i][1] == self.index_y:
                        log.printInfo(f"Got breakpoint {i} {self.breakpoint[i]}")
                        self.show_status()
                        self.breakpoint.remove(self.breakpoint[i])
                        self.interrupted = True
                if self.interrupted:
                    break
                self.interpret(self.code[self.index_y][self.index_x])
                if self.halted:
                    return self.reason
                if self.current_direction == RIGHT:
                    self.index_x += 1
                    if self.index_x >= self.width:
                        self.halted = True
                        self.reason = "Beam was out of range"
                elif self.current_direction == LEFT:
                    self.index_x -= 1
                    if self.index_x < 0:
                        self.halted = True
                        self.reason = "Beam was out of range"
                elif self.current_direction == UP:
                    self.index_y -= 1
                    if self.index_y < 0:
                        self.halted = True
                        self.reason = "Beam was out of range"
                elif self.current_direction == DOWN:
                    self.index_y += 1
                    if self.index_y >= self.height:
                        self.halted = True
                        self.reason = "Beam was out of range"
        else:
            for _ in range(count):
                for i in range(len(self.breakpoint)):
                    if self.breakpoint[i][0] == self.index_x and self.breakpoint[i][1] == self.index_y:
                        log.printInfo(f"Got breakpoint {i} {self.breakpoint[i]}")
                        self.show_status()
                        self.interrupted = True
                if self.interrupted:
                    break
                self.interpret(self.code[self.index_y][self.index_x])
                if self.halted:
                    return self.reason
                if self.current_direction == RIGHT:
                    self.index_x += 1
                    if self.index_x >= self.width:
                        self.halted = True
                        self.reason = "Beam was out of range"
                elif self.current_direction == LEFT:
                    self.index_x -= 1
                    if self.index_x < 0:
                        self.halted = True
                        self.reason = "Beam was out of range"
                elif self.current_direction == UP:
                    self.index_y -= 1
                    if self.index_y < 0:
                        self.halted = True
                        self.reason = "Beam was out of range"
                elif self.current_direction == DOWN:
                    self.index_y += 1
                    if self.index_y >= self.height:
                        self.halted = True
                        self.reason = "Beam was out of range"


log.printInfo('For help, type "help".')
p = None

while True:
    if p:
        prefix = f"{set_color('green', 1)}beamdbg> {set_color(0)}"
        # show_code(p.index_x, p.index_y)
        # print(f"Current index : {p.index_x}, {p.index_y}")
        # print(f"Current value of 'Beam' : {p.beam}")
        # print(f"Current value of 'Store' : {p.store}")
    else:
        prefix = f"{set_color('red', 1)}beamdbg> {set_color(0)}"
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
        if not p:
            log.printWarning("Process not found")
            continue
        if len(param) != 2:
            log.printWarning("Usage: b [x] [y]")
        else:
            try:
                p.breakpoint.append([int(param[0]), int(param[1])])
                log.printInfo(f"Added breakpoint at [{param[0]}, {param[1]}]")
            except ValueError:
                log.printWarning("ValueError")
                log.printWarning("Usage: b [x] [y]")
    elif cmd == "ni":
        if not p:
            log.printWarning("Process not found")
            continue
        if not param:
            reason = p.run(1)
            if reason:
                log.printInfo(
                    f"Process exited with reason: {set_color('yellow')}{reason}{set_color(0)}"
                )
                p = None
            else:
                p.show_status()
        else:
            try:
                reason = p.run(int(param[0]))
                if reason:
                    log.printInfo(
                        f"Process exited with reason: {set_color('yellow')}{reason}{set_color(0)}"
                    )
                    p = None
                else:
                    p.show_status()
            except ValueError:
                log.printWarning("ValueError")
                log.printWarning("Usage: ni <steps>")
                continue

    elif cmd == "start":
        print()
        log.printInfo("Starting to debug...")
        readable_chars = "><^v+-@:/\\!?|_HSLsgPpun`')(r\n "
        try:
            log.printInfo(
                f"Loading code file {set_color('blue')}{code_file}{set_color(0)}..."
            )
            with open(code_file, "r") as f:
                code = f.read()
            log.printInfo(
                f"Code file successfully loaded {set_color('blue')}{code_file}{set_color(0)}"
            )
        except FileNotFoundError:
            log.printError(
                f"Code file not found {set_color('blue')}{code_file}{set_color(0)}", 2
            )

        try:
            log.printInfo(
                f"Loading input file {set_color('green')}{input_file}{set_color(0)}..."
            )
            with open(input_file, "r") as f:
                inp = f.read()
            log.printInfo(
                f"Input file successfully loaded {set_color('green')}{input_file}{set_color(0)}"
            )
        except FileNotFoundError:
            log.printError(
                f"Cannot found input file {set_color('green')}{input_file}{set_color(0)}",
                3,
            )
        for c in code:
            if c not in readable_chars:
                log.printWarning(
                    f"Found unreadable char {set_color('red')}{c}{set_color(0)} in code, it will be ignored."
                )
        splitted_code = code.split("\n")
        height = len(splitted_code)
        width = max([len(l) for l in splitted_code])
        log.printInfo(f"Code height: {height}")
        log.printInfo(f"Code width: {width}")
        output_fp = open(output_file, "w")
        output_fp.close()
        p = Process(splitted_code, inp, height, width)
        p.show_status()
        print()
    elif cmd == "run":
        if not p:
            log.printWarning("Process not found")
            continue
        reason = p.run()
        if reason:
            log.printInfo(
                f"Process exited with reason: {set_color('yellow')}{reason}{set_color(0)}"
            )
            p = None
    elif cmd == "mem":
        if not p:
            log.printWarning("Process not found")
            continue
        else:
            show_memory(p.modified_memory_index, p.memory, p.beam, p.store)
    elif cmd == "stop":
        p = None
    elif cmd == "exit" or cmd == "quit":
        exit(0)
    else:
        log.printInfo('Unknown command. type "help" for help.')
