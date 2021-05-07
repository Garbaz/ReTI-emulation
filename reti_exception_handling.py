from sys import stderr


def eprint(instr, instr_args, exception_inst, *args, **nargs):
    print("ERROR at `"
          + instr + " " + " ".join(instr_args) + "` ::", file=stderr)
    print("  " + exception_inst.__class__.__name__ +"(\"" + str(exception_inst) + "\")", file=stderr)
    print("  -- ", *args, **nargs, file=stderr)

