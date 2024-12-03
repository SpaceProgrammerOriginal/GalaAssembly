# What is GalaAssembly?
GalaAssembly is a series of compilers for my custom CPUs assembly using the family of arquitecture Galaicum (a custom arquitecture).

Actually it includes the compiler for the arquitecture Galaicum16v1_1 for my 16-bit cpu Gala I, and in the future it will include the compiler
for the arquitecture Galaicum32v2_1 for my comming soon 32-bit cpu Gala II

## Where to find the CPUs

The CPUs will be available to download comming really soon, they will be in the filetype .circ, made in Logisim-evolution.

## The numbers (of the arquitectures), what do they mean?

For those with curiosity the numbers of the arquitectures names have meaning behing them:

```
Galaicum    16  v1  _1
            |   |    ↓
            |   ↓    this is the first revision of this version of the arquitecture
            ↓   this is the first version of the arquitecture
            the cpu is 16-bit
```

so then, for the cpu Gala II with Galaicum32v2_1:

```
Galaicum    32  v2  _1
            |   |    ↓
            |   ↓    this is the first revision of this version of the arquitecture
            ↓   this is the second version of the arquitecture
            the cpu is 32-bit
```

Note also that that I normally shortcut this names only preserving the numbers and the first letter:

```
Galaicum16v1_1 --> G1611
Galaicum32v2_1 --> G3221
```

## How to compile something with this?

This compiler is made for maximum ease of use so that shouldn't be a big problem.
The first thing to consider is the instructions of the arquitecture:

### Galaicum16v1_1

*(More information of the Galaicum16v1_1 will be uploaded soon)*

|Instruction Name|Description|Parameters|**Opcode**|
|----------------|-----------|----------|----------|
|Halt            |Stops all execution|-|HALT|
|Write Upper     |Writes upper 8 bits to a register|reg [str], val [0-255]|WUPP|
|Write Lower     |Writes lower 8 bits to a register|reg [str], val [0-255]|WLOW|
|Write RAM       |Writes to a register value to RAM|reg address [str], reg to write [str]|WRAM|
|Read RAM        |Loads a RAM value to a register|reg address [str], reg to load [str]|RRAM|
|Complex Jump    |Jump if true condition between 2 registers<br>The conditions are: ">", "==", "<", "<=", "!=", ">=", "==0", "<0", "!=0", ">0"<br>- In the case that the condition is the four last, the address used is RegB and comparison made in regA<br>- In other cases the address in register p0|regA [str], cond., regB [str]|CJUMP|
|ALU             |Performs one an ALU operation with regs alu-a, alu-b and outputs to alu-r|op [str]|ALU|
|Copy            |Copies from one to another register|fromReg [str], toReg [str]|COPY|

There are also comments with `#`, but note that they only work in blank lines.

#### Example code

This code computes the Fibonacci sequence (maximum explicit possible) to the number in r0 specified (in this case 10):

```
#number of iterations
WUPP r0, 0;
WLOW r0, 10;

#iterator
WUPP r1, 0;
WLOW r1, 0;

#"add one" variable in iterator
WUPP r2, 0;
WLOW r2, 1;

#store result 1
WUPP r3, 0;
WLOW r3, 1;

#store result 2
WUPP r4, 0;
WLOW r4, 1;

#store the address of the loop start (yes, you have to manually count)
WUPP p0, 0;
WLOW p0, 12;

#loop
    #adding
    COPY r3, alu-a;
    COPY r4, alu-b;
    ALU add;
    #copy result + push back
    COPY r3, r4; 
    COPY r3, alu-r;
    #add to iterator
    COPY r1, alu-a;
    COPY r2, alu-b;
    ALU add;
    COPY alu-r, r1;
    CJUMP r1 < r0;
#end of the loop

#saving result to ram
    #selecting address
    WUPP p0, 255;
    WLOW p0, 255;
    #saving
    WRAM p0, r3;

HALT; #halting
```

### Direct compile...

Once you have a file with code you can compile directly calling `GalaAssembly.ARQUITECTURE_NAME.compiler.full_compile()`
where ARQUITECTURE_NAME is G1611 until now, because Galaicum16v1_1 is the only arquitecture available.

`full_compile()` does directly read a file and save the compiled code in another file.

### ...or compile by parts

If you want to compile by parts, the steps to fully compile a file are:

```
1- read the file
2- tokenize the code with:
    GalaAssembly.ARQUITECTURE_NAME.text.tokenize_code(code)
3- compile tokenized:
    GalaAssembly.ARQUITECTURE_NAME.compiler.compile_tokenized(tokenized_code)
4- save the result as a ram image that can be read by Logisim:
    GalaAssembly.ARQUITECTURE_NAME.text.save_ram_image(filename, compiled_code)
```
