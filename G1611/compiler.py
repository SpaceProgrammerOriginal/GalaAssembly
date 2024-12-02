"""
Compiler of the official Galaicum16v1_1 arquitecture

Supported CPUs: Gala I
"""

REGISTER_NAMES = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "alu-a", "alu-b", "alu-r", "pc", "ir", "p0"]
ALU_MODES = ["add", "sub", "mul", "div", "shift-left", "shift-right", "rot-left", "rot-right", ">", "==", "<", "not", "and", "or", "xor", "no-op"]
CJUMP_MODES = [">", "==", "<", "==0", "<0", "<=", "!=", ">=", "!=0", ">0"]

from . import text as _text
import os as _os


def _to_bits(integer : int, bits : int = 4):
    """
    Gets a bits representation (in str) of a certain lenght of the passed integer.
    """

    return bin(integer).removeprefix("0b").rjust(bits, "0")


def compile_tokenized(tokenized_code : list[list[str]]):

    """
    Compiles to a string a tokenized code input
    """

    compiled_file = "" #where the result is stored

    for command in tokenized_code:

        compiled_command = ""

        match command[0].upper():

            case "HALT":
                compiled_command += "0000"
            case "WUPP":
                compiled_command += "0001"
                compiled_command += _to_bits(REGISTER_NAMES.index(command[1]))
                compiled_command += _to_bits(int(command[2]), bits=8)

            case "WLOW":
                compiled_command += "0010"
                compiled_command += _to_bits(REGISTER_NAMES.index(command[1]))
                compiled_command += _to_bits(int(command[2]), bits=8)

            case "WRAM":
                compiled_command += "0011"
                compiled_command += _to_bits(REGISTER_NAMES.index(command[1]))
                compiled_command += _to_bits(REGISTER_NAMES.index(command[2]))

            case "RRAM":
                compiled_command += "0100"
                compiled_command += _to_bits(REGISTER_NAMES.index(command[1]))
                compiled_command += _to_bits(REGISTER_NAMES.index(command[2]))

            case "CJUMP":
                compiled_command += "0101"
                compiled_command += _to_bits(REGISTER_NAMES.index(command[1]))

                #get the first 3 bits (so up to 7) to binary and then the 4th bit used after for invert
                idx = CJUMP_MODES.index(command[2])

                compiled_command += _to_bits(idx & 0b111, bits=3)
                compiled_command += _to_bits(REGISTER_NAMES.index(command[3]))
                compiled_command += _to_bits(idx & 0b1000, bits=1)
            case "ALU":
                compiled_command += "0110"
                compiled_command += _to_bits(ALU_MODES.index(command[1]))
            case "COPY":
                compiled_command += "0111"
                compiled_command += _to_bits(REGISTER_NAMES.index(command[1]))
                compiled_command += _to_bits(REGISTER_NAMES.index(command[2]))
            case _:
                raise ValueError("That command does not exist")
            
        #justify size to 16-bit (left justify)
        compiled_command = compiled_command.ljust(16, "0")

        #convert to hex and put to compiled_file
        compiled_file += hex(int(compiled_command, 2)).removeprefix("0x").ljust(4, "0") + "\n"

    return compiled_file

def full_compile(code_filename : _os.PathLike, output_filename : _os.PathLike):

    """
    Does all the full process of compilation:

    1- get code
    2- tokenize code
    3- compile code
    4- save compiled to filename
    """

    with open(code_filename, "r") as file:
        code = file.read()

    tokenized = _text.tokenize_code(code)

    compiled = compile_tokenized(tokenized)

    _text.save_ram_image(output_filename, compiled)

    