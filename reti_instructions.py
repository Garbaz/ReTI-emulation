from reti_exception_handling import eprint


# ------------------------- EXPORT -------------------------

INSTRUCTIONS = {}


def exec_instruction(reg, mem, instr, *args):
    """
    Execute a single instruction `instr`, modifying `reg` & `mem`
    `reg : dict[str,int]`
        The device's registers; Has to contain "ACC","IN1","IN2","PC"
    `mem : dict[int,int]`
        The device's memory; Any cells read from have to exist before-hand
    `instr : str`
        The instruction name
    `*args: str`
        The arguments for the given instruction
    """

    # `args` are reversed, since arguments without a default value have to come before arguments with.
    # This is to allow for instructions taking a register to default to ACC,
    # and JUMP to default to unconditional jump, without any dirty functool shenanigans
    try:
        f = INSTRUCTIONS[instr]
    except KeyError as inst:
        eprint(instr, args, inst, "Invalid instruction.")
        exit(1)
    try:
        return f(reg, mem, *(reversed(args)))
    except ValueError as inst:
        eprint(instr, args, inst, "An argument that should be a number isn't.")
        exit(1)
    except TypeError as inst:
        eprint(instr, args, inst, "An instruction has the wrong number of arguments.")
        exit(1)
    except KeyError as inst:
        eprint(instr, args, inst, "Invalid register name, reading from empty memory or invalid comparator for jump.")
        exit(1)


# ------------------------- LOCAL -------------------------


def _gen_instructions():
    global INSTRUCTIONS

    COMPARATORS = {">": lambda a: a > 0,
                   "=": lambda a: a == 0,
                   ">=": lambda a: a >= 0,
                   "<": lambda a: a < 0,
                   "!=": lambda a: a != 0,
                   "<=": lambda a: a <= 0,
                   "": lambda a: True}

    # ====== instructions ======

    # --- LOAD instructions ---

    def LOAD(reg, mem, i, D="ACC"):
        reg[D] = mem[int(i)]
        return D == "PC"

    def LOADIN1(reg, mem, i, D="ACC"):
        reg[D] = mem[int(i)+reg["IN1"]]
        return D == "PC"

    def LOADIN2(reg, mem, i, D="ACC"):
        reg[D] = mem[int(i)+reg["IN2"]]
        return D == "PC"

    def LOADI(reg, mem, i, D="ACC"):
        reg[D] = int(i)
        return D == "PC"

    # --- STORE instructions ---

    def STORE(reg, mem, i):
        mem[int(i)] = reg["ACC"]

    def STOREIN1(reg, mem, i):
        mem[int(i)+reg["IN1"]] = reg["ACC"]

    def STOREIN2(reg, mem, i):
        mem[int(i)+reg["IN2"]] = reg["ACC"]

    def MOVE(reg, mem, D, S):
        reg[D] = reg[S]
        return D == "PC"

    # --- Compute instructions (immediate) ---

    def SUBI(reg, mem, i, D="ACC"):
        reg[D] -= int(i)
        return D == "PC"

    def ADDI(reg, mem, i, D="ACC"):
        reg[D] += int(i)
        return D == "PC"

    def OPLUSI(reg, mem, i, D="ACC"):
        reg[D] ^= int(i)
        return D == "PC"

    def ORI(reg, mem, i, D="ACC"):
        reg[D] |= int(i)
        return D == "PC"

    def ANDI(reg, mem, i, D="ACC"):
        reg[D] &= int(i)
        return D == "PC"

    # --- Compute instructions (memory) ---

    def SUB(reg, mem, i, D="ACC"):
        reg[D] -= mem[int(i)]
        return D == "PC"

    def ADD(reg, mem, i, D="ACC"):
        reg[D] += mem[int(i)]
        return D == "PC"

    def OPLUS(reg, mem, i, D="ACC"):
        reg[D] ^= mem[int(i)]
        return D == "PC"

    def OR(reg, mem, i, D="ACC"):
        reg[D] |= mem[int(i)]
        return D == "PC"

    def AND(reg, mem, i, D="ACC"):
        reg[D] &= mem[int(i)]
        return D == "PC"

    # --- Jump instructions ---

    def NOP(reg, mem):
        pass

    def JUMP(reg, mem, i, c=""):
        if COMPARATORS[c](reg["ACC"]):
            reg["PC"] += int(i)
            return True

    # --- Special instructions ---

    def _TEST(reg, mem, *args):
        print("TEST", args)

    def _PRINT(reg, mem, i_or_D="ACC"):
        if i_or_D.isdecimal():
            print("~~ M(" + i_or_D + ") = " + str(mem[int(i_or_D)]))
        else:
            print("~~ " + i_or_D + " = " + str(reg[i_or_D]))

    def _INPUT(reg, mem, i_or_D="ACC"):
        if i_or_D.isdecimal():
            mem[int(i_or_D)] = int(input(">> M(" + i_or_D + ")" + " = "))
        else:
            reg[i_or_D] = int(input(">> " + i_or_D + " = "))

    # ============

    # Generate `INSTRUCTIONS` list of instructions from local functions
    for key, value in locals().items():
        if callable(value) and value.__module__ == __name__:
            INSTRUCTIONS[key] = value


_gen_instructions()
