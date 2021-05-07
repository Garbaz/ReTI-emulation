
from reti_instructions import exec_instruction
from sys import argv, exit

HELP_MSG = """
USAGE
    python3 reti_emulator.py [OPTIONS] FILE

with FILE being the name of a file containing ReTI instructions.

OPTIONS
    -h | --help
        Print this help message.

    -v | --verbose
        Details of about progress are printed during execution.

    -s | --stepping
        Pause execution after every instruction and wait for ENTER

    -r | --no-debug
        Debug instructions and end-state (see README.md) are NOT executed.


For further information, please look in README.md.
"""


# ====== Consts ======

COMMENT_DELIMS = ["#", "//"]
DEBUG_DELIM = ";"


# ====== Parameters ======

# DO NOT EDIT, these are set via command-line arguments!
# Type `python3 reti_emulator.py --help` in command line for info.
VERBOSE = False
DEBUG = True
STEPPING = False


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
    print("Memory:      ", end="")
    for k, v in mem.items():
        print(f'M({k:< 4}) = {v:< 4} , ', end="")
    print()


# ====== Interpreter ======

def interpret_line(line):
    """
    Interpret and execute a single line
    `line : tuple[str,str]``
        the instruction and debug instruction to execute
    `-> bool`
        True if PC should NOT be incremented, None or False otherwise
    """

    instr = line[0]
    debug = line[1]

    split = instr.split()

    ret = exec_instruction(reg, mem, *split)

    if DEBUG and debug != "":
        print("~ Debug(" + debug + "):   ", end="")
        interpret_line((debug, ""))

    return ret


def interpret(lines):
    """
    Interpret and execute a multiple lines
    `lines : list[tuple[str,str]]`
         the instruction/debug-instruction pairs to execute
    """
    stats_steps = 0
    stats_jumps = 0
    if STEPPING:
        print("~~~~~~ Stepping mode enabled! Use ENTER to step through code ~~~~~~")
    while 0 <= reg["PC"] and reg["PC"] < len(lines):
        if STEPPING:
            input()  # Wait for input before executing instruction

        if VERBOSE:
            # Print information about current state and instruction
            print("-"*80)
            print_state_compact()
            print()
            print("Instruction:", lines[reg["PC"]][0])

        if not interpret_line(lines[reg["PC"]]):
            reg["PC"] += 1
        else:
            stats_jumps += 1
        stats_steps += 1

    if DEBUG:
        print()
        print("~~~~~~ Reached end of code or jumped to invalid address. Final state: ~~~~~~")
        print()
        print_state()
        print()
        print("Stats:")
        print("    Total steps  : ", stats_steps)
        print("    Jumps taken  : ", stats_jumps)
        print("    Memory usage : ",len(mem))
        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# ====== Code handling ======

def clean_code(code):
    """
    Remove comments and split into instructions/debug-instructions
    Lines containing no instruction are removed
    `code : str`
        The code e.g. as read from a file
    `-> list[tuple[str,str]]`
        The instruction/debug-instruction pairs
    """

    ret = []
    for line in code.splitlines():

        # Split off and clean debug instruction
        debug = line.split(DEBUG_DELIM)
        if len(debug) > 1:
            debug = debug[-1].strip()
        else:
            debug = ""

        # Remove comments and clean instruction
        for c in COMMENT_DELIMS:
            line = line.split(c, 1)[0]
        line = line.strip()
        if line != "":
            ret.append((line, debug))
    return ret


def load_code(filename):
    with open(filename, "r") as file:
        return file.read()


# ====== Main ======
if __name__ == "__main__":
    if len(argv) == 1:
        print(HELP_MSG)
        exit(1)
    else:
        filename = ""

        for a in argv:
            if not a.startswith("-"):
                filename = a
            else:
                if a in ["-h", "--help"]:
                    print(HELP_MSG)
                    exit(0)
                elif a in ["-v", "--verbose"]:
                    VERBOSE = True
                elif a in ["-r", "--no-debug"]:
                    DEBUG = False
                elif a in ["-s", "--stepping"]:
                    STEPPING = True

        code = load_code(filename)
        lines = clean_code(code)
        interpret(lines)
