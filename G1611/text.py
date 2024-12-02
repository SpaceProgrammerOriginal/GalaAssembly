import re as _re
import os as _os

def tokenize_code(code : str) -> list[list[str]]:

    """
    Converts the code to a splitted understandable list for the compiler
    """

    #this function comes from the Simply programming language, made by me :)

    comment_split = code.split("#") #split by comentaris

    comment_split = [splitted.split("\n") for splitted in comment_split] #split in lines, as comments cover full lines

    #now each first element in sublist is a comment, so delete:
    comment_split = [splitted[1:] for splitted in comment_split]

    #now flatten the list
    flatten = [element for sublist in comment_split for element in sublist]

    #put all the code without comments together + strip
    fixed_code = "".join(flatten).strip()
    
    #now starts the regular parsing
    commands = fixed_code.split(";") #separe by commands

    #split parameters from opcodes
    commands = [command.split(",") for command in commands if command != ""] #delete empty str and split by comma

    #split opcode of first parameter
    for idx in range(len(commands)):
        sub_command = commands[idx][0].lstrip().split(" ") #deleting tabing with the lstrip()
        commands[idx][0] = sub_command[0] #the opcode set it to the first argument
        commands[idx].insert(1, "".join(sub_command[1:])) #the rest insert directly

    commands = [[sub_command.strip() for sub_command in command if sub_command != ""] for command in commands] #strip

    #special split for CJUMP op, as no commas:

    for idx in range(len(commands)):
        if commands[idx][0] == "CJUMP":
            match = _re.match(r"^(.+?\b)(.+?\b)(.+?\b)", commands[idx][1]) #separate text from operators with regex

            #get the groups and append
            match_groups = match.groups()
            commands[idx].pop()
            commands[idx].append(match_groups[0])
            commands[idx].append(match_groups[1])
            commands[idx].append(match_groups[2])

    return commands
    
def save_ram_image(filename : _os.PathLike, compiled_code : str):

    """
    Puts a compiled code in hexadecimal to a file to be read by Logisim as a ram image.
    Format used: v2.0 raw
    """

    FORMAT = "v2.0 raw\n"

    with open(filename, "w") as file:
        file.write(FORMAT + compiled_code)

