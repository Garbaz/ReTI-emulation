# ReTI Emulation

An emulator for the fictional processor "ReTI" from the lecture [Technische Informatik](https://abs.informatik.uni-freiburg.de/src/teach_main.php?id=158) at the University Freiburg.

### Features

* Full instruction set (as defined on Slide 19 of "k23-Anwendung_ReTI.pdf")
* Special instructions for terminal interaction (see below)
* Optional verbose live view of the register/memory state
* Comments
* Option for adding debug instruction at the end of lines


### Usage

```
    python3 reti_emulator.py [OPTIONS] FILE

with FILE being the name of a file containing ReTI instructions.

OPTIONS
    -h | --help
        Print this help message.
    
    -v | --verbose
        Details of about progress are printed during execution.
```


### Instructions

```
## Load instructions:

LOAD D i            # D = M(i)
LOADIN1 D i         # D = M(i+IN1)
LOADIN2 D i         # D = M(i+IN2)
LOADI D i           # D = i

## Store instructions:

STORE i             # M(i) = ACC
STOREIN1 i          # M(i+IN2) = ACC
STOREIN2 i          # M(i+IN2) = ACC
MOVE S, D           # D = S

## Compute instructions (immediate):

SUBI D i            # D = D - i
ADDI D i            # D = D + i
OPLUSI D i          # D = D ^ i
ORI D i             # D = D | i
ANDI D i            # D = D & i

## Compute instructions (memory):

SUB D i             # D = D - M(i)
ADD D i             # D = D + M(i)
OPLUS D i           # D = D ^ M(i)
OR D i              # D = D | M(i)
AND D i             # D = D & M(i)

## Jump instructions:

NOP                 # Does nothing
JUMP c, i           # if ACC `c` 0: PC = PC + i   (c has to one of [< , > , <= , >= , = , !=])
JUMP i              # PC + i

## Special instructions (Note leading underscore!):

_PRINT i_or_D       # Prints the value at M(i) if given a number or to register D
_INPUT i_or_D       # Reads from stdin and saves value to M(i) if given a number or to register D
```

### Comments

Anything after a `#` or a `//` is considered a comment, and will be ignored for execution (except for debug instructions, see below).

**Example:**
```
JUMP 1      # This is a comment
JUMP -1     // This also is a comment
```


### Debug instructions

At the end of a line, after the instruction *and comment*, a `;` followed by another instruction can be added.
This instruction will be executed after the line it is on, but, importantly, *does not count as an instruction for the program counter/jumps*.
This way it is possible to add instructions for the purpose of debugging, which do not require readjusting the parameters of `JUMP` instructions.

**Example:**
```
LOADI ACC 5     # The comment comes first       ;_PRINT ACC
JUMP -1         # This jump still jumps to the instruction above, with or without the _PRINT

```