# ReTI Emulation

An emulator for the fictional processor "ReTI" from the lecture [Technische Informatik](https://abs.informatik.uni-freiburg.de/src/teach_main.php?id=158) at the University Freiburg.

## Features

* Full instruction set (as defined on Slide 19 of "k23-Anwendung_ReTI.pdf")
* Special instructions for terminal interaction (see below)
* Live view of register/memory state
* Stepping
* Comments
* Error handling
* A way to add debug instruction without breaking jumps (see below)


## Usage

```
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
```

## Instructions

For all instructions taking a register name D, the register name
can be left out, in which case the ACC register will be used by default.
(Excluding the `MOVE` instruction)

### NOTE: The JUMP argument

As would be the case in real hardware, `JUMP`s go by instructions, not by lines. Any lines that do not contain an instruction are discarded before execution (even if they contain a comment), so make sure the the arguments for `JUMP` instructions are set correctly.

**Example:**
```py
ADDI ACC 1
# With a comment or without...

# ... these "empty" lines are discarded ...
JUMP -1 # ... so this `JUMP` still jumps to the `ADDI` in the first line
```

### Full list of instructions

```py
## Load instructions:

LOAD [D] i          # D = M(i)
LOADIN1 [D] i       # D = M(i+IN1)
LOADIN2 [D] i       # D = M(i+IN2)
LOADI [D] i         # D = i

## Store instructions:

STORE i             # M(i) = ACC
STOREIN1 i          # M(i+IN2) = ACC
STOREIN2 i          # M(i+IN2) = ACC
MOVE S, D           # D = S

## Compute instructions (immediate):

SUBI [D] i          # D = D - i
ADDI [D] i          # D = D + i
OPLUSI [D] i        # D = D ^ i
ORI [D] i           # D = D | i
ANDI [D] i          # D = D & i

## Compute instructions (memory):

SUB [D] i           # D = D - M(i)
ADD [D] i           # D = D + M(i)
OPLUS [D] i         # D = D ^ M(i)
OR [D] i            # D = D | M(i)
AND [D] i           # D = D & M(i)

## Jump instructions:

NOP                 # Does nothing
JUMP c, i           # if ACC `c` 0: PC = PC + i
                    # (c has to one of [< , > , <= , >= , = , !=])

JUMP i              # PC = PC + i

## Special instructions (Note leading underscore!):

_PRINT i_or_D       # Prints the value in M(i) or register D to stdout
_INPUT i_or_D       # Reads from stdin and stores the value to M(i) or register D
```

## Comments

Anything after a `#` or a `//` is considered a comment, and will be ignored for execution (except for debug instructions, see below).

**Example:**
```py
JUMP 1      # This is a comment
```
```c
JUMP -1     // This also is a comment
```


## Special instructions

Special instructions expand the normal instruction set to fascilitate various convenience functions. All special instructions begin with an underscore ("\_").
The following special instructions are implemented:

### \_PRINT
```
_PRINT i_or_D
```

If given a number i (e.g. `_PRINT 33`) the value in M(i) will be printed to stdout.
If given a register name (e.g. `_PRINT ACC`), the value in that register will be printed to stdout.

### \_INPUT
```
_INPUT i_or_D
```

If given a number i (e.g. `_INPUT 30`) a number will be read from stdin and stored in M(i).
If given a register name (e.g. `_INPUT ACC`), a number will be read from stdin and stored in that register.


## Debug instructions

At the end of a line, after the instruction *and comment*, a `;` followed by another instruction can be added.
This instruction will be executed after the line it is on, but, importantly, *does not count as an instruction for the program counter/jumps*.
This way it is possible to add instructions for debugging, without requiring adjustment of the parameters of `JUMP` instructions.


**Example:**
```py
# The `_PRINT ACC` at the end of the line is executed,
# but does not count as it's own instruction in regards
# to the program counter, so the following `JUMP` still
# works as intended.

ADDI ACC 1     # The comment comes first       ;_PRINT ACC
JUMP -1         # Jump still jumps to `LOADI`

```


## TODO

- [ ] Fancy print/input (?) (something like `_PRINT "The current value is " ACC`)
- [x] Error handling and comments
- [x] Stats (number of cycles, memory usage, jumps...) [live? total?]
