import re

def tokenize_code(code : str) -> list[list[str]]:

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

    print(commands)

    #split opcode of first parameter
    for idx in range(len(commands)):
        sub_command = commands[idx][0].lstrip().split(" ") #deleting tabing with the lstrip()
        commands[idx][0] = sub_command[0] #the opcode set it to the first argument
        commands[idx].insert(1, "".join(sub_command[1:])) #the rest insert directly

    print()
    print(commands)

    commands = [[sub_command.strip() for sub_command in command if sub_command != ""] for command in commands] #strip

    #special split for CJUMP op, as no commas:

    for idx in range(len(commands)):
        if commands[idx][0] == "CJUMP":
            print()
            print(commands[idx][1])
            match = re.match(r"^(.+?\b)(.+?\b)(.+?\b)", commands[idx][1]) #separate text from operators with regex

            #get the groups and append
            match_groups = match.groups()
            commands[idx].pop()
            commands[idx].append(match_groups[0])
            commands[idx].append(match_groups[1])
            commands[idx].append(match_groups[2])

    return commands
    
