

# ------------------------- EXPORT -------------------------

INSTRUCTIONS = {}


def exec_instruction(reg: dict[str, int], mem: dict[int, int], instr: str, *args) -> bool:
    return INSTRUCTIONS[instr](reg, mem, *args)


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

    def LOAD(reg, mem, D, i):
        reg[D] = mem[int(i)]
        return D == "PC"

    def LOADIN1(reg, mem, D, i):
        reg[D] = mem[int(i)+reg["IN1"]]
        return D == "PC"

    def LOADIN2(reg, mem, D, i):
        reg[D] = mem[int(i)+reg["IN2"]]
        return D == "PC"

    def LOADI(reg, mem, D, i):
        reg[D] = int(i)
        return D == "PC"

    # --- STORE instructions ---

    def STORE(reg, mem, i):
        mem[int(i)] = reg["ACC"]

    def STOREIN1(reg, mem, i):
        mem[int(i)+reg["IN1"]] = reg["ACC"]

    def STOREIN2(reg, mem, i):
        mem[int(i)+reg["IN2"]] = reg["ACC"]

    def MOVE(reg, mem, S, D):
        reg[D] = reg[S]
        return D == "PC"

    # --- Compute instructions (immediate) ---

    def SUBI(reg, mem, D, i):
        reg[D] -= int(i)
        return D == "PC"

    def ADDI(reg, mem, D, i):
        reg[D] += int(i)
        return D == "PC"

    def OPLUSI(reg, mem, D, i):
        reg[D] ^= int(i)
        return D == "PC"

    def ORI(reg, mem, D, i):
        reg[D] |= int(i)
        return D == "PC"

    def ANDI(reg, mem, D, i):
        reg[D] &= int(i)
        return D == "PC"

    # --- Compute instructions (memory) ---

    def SUB(reg, mem, D, i):
        reg[D] -= mem[int(i)]
        return D == "PC"

    def ADD(reg, mem, D, i):
        reg[D] += mem[int(i)]
        return D == "PC"

    def OPLUS(reg, mem, D, i):
        reg[D] ^= mem[int(i)]
        return D == "PC"

    def OR(reg, mem, D, i):
        reg[D] |= mem[int(i)]
        return D == "PC"

    def AND(reg, mem, D, i):
        reg[D] &= mem[int(i)]
        return D == "PC"

    # --- Jump instructions ---

    def NOP(reg, mem):
        pass

    def JUMP(reg, mem, c, i=None):
        if i == None:
            reg["PC"] += int(c)  # Not pretty, but if only one argument is given `c` is 'i'...
            return True
        elif COMPARATORS[c](reg["ACC"]):
            reg["PC"] += int(i)
            return True

    # --- Special instructions ---

    def _TEST(reg, mem, *args):
        print("TEST", args)

    def _PRINT(reg, mem, i_or_D):
        if i_or_D.isdecimal():
            print(">>>>>>  M(" + i_or_D + ") = " + str(mem[int(i_or_D)]))
        else:
            print(">>>>>>  " + i_or_D + " = " + str(reg[i_or_D]))

    def _INPUT(reg, mem, i_or_D):
        if i_or_D.isdecimal():
            mem[int(i_or_D)] = int(input(">>>>>>  M(" + i_or_D + ")" + " = "))
        else:
            reg[i_or_D] = int(input(">>>>>>>  " + i_or_D + " = "))

    # ============

    # Generate `INSTRUCTIONS` list of instructions from local functions
    for key, value in locals().items():
        if callable(value) and value.__module__ == __name__:
            INSTRUCTIONS[key] = value


_gen_instructions()
