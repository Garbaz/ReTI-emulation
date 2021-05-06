
from reti_instructions import exec_instruction
from sys import argv, exit

_HELP = """
USAGE
    python3 reti_emulator.py [OPTIONS] FILE

with FILE being the name of a file containing ReTI instructions.

OPTIONS
    -h | --help
        Print this help message.
    
    -v | --verbose
        Details of about progress are printed during execution.


For further information, please look in README.md.
"""


# ====== Consts ======

COMMENT_DELIMS = ["#", "//"]
DEBUG_DELIM = ";"

VERBOSE = False


# ====== Global ReTI state ======

reg = {"ACC": 0, "IN1": 0, "IN2": 0, "PC": 0}
mem = {}


def print_state():
    print("Registers:")
    print("    ACC =", reg["ACC"])
    print("    IN1 =", reg["IN1"])
    print("    IN2 =", reg["IN2"])
    print("    PC  =", reg["PC"])
    print("Memory:")
    print("    Address    | Value")
    for k, v in mem.items():
        print(f'    {k: 10} | {v: 10}')


def print_state_compact():
    print(f'Registers:   ACC = {reg["ACC"]:< 4} , IN1 = {reg["IN1"]:< 4} , IN2 = {reg["IN2"]:< 4} , PC = {reg["PC"]:< 4}')
    print( "Memory:      ", end="")
    for k, v in mem.items():
        print(f'M({k:< 4}) = {v:< 4} , ', end="")
    print()


# ====== Interpreter ======

def interpret_line(line: (str, str)) -> bool:
    global reg, mem
    debug = line[1]
    line = line[0]
    split = line.split()

    ret = None
    if len(split) >= 1:
        ret = exec_instruction(reg, mem, *split)

    if debug != "":
        print("~ Debug(" + debug + "):   ", end="")
        interpret_line((debug, ""))

    return ret


def interpret(lines: list[(str, str)]):
    while 0 <= reg["PC"] and reg["PC"] < len(lines):
        if(VERBOSE):
            print("-"*80)
            print_state_compact()
            print("Instruction:", lines[reg["PC"]][0])
            print()
        if not interpret_line(lines[reg["PC"]]):
            reg["PC"] += 1
    print()
    print("~~~~~~ Reached end of code or jumped to invalid address. Final state: ~~~~~~")
    print()
    print_state()
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# ====== Code handling ======

def clean_code(code: str) -> list[(str, str)]:
    ret = []
    for line in code.splitlines():
        debug = line.split(DEBUG_DELIM)
        if len(debug) > 1:
            debug = debug[-1].strip()
        else:
            debug = ""

        for c in COMMENT_DELIMS:
            line = line.split(c, 1)[0]
        line = line.strip()
        ret.append((line, debug))
    return ret


def load_code(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read()


# ====== Main ======
if __name__ == "__main__":
    if len(argv) == 1:
        print(_HELP)
        exit(1)
    else:
        filename = ""

        for a in argv:
            if not a.startswith("-"):
                filename = a
            else:
                if a in ["-h", "--help"]:
                    print(_HELP)
                    exit(0)
                elif a in ["-v", "--verbose"]:
                    VERBOSE = True

        code = load_code(filename)
        lines = clean_code(code)
        interpret(lines)
