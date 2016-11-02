// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here

(LOOP)

@R0                             //Decreasing the counter in R1 register.
M = M - 1;
D = M;

@END
D;JLT                          //Ending the function if D register counter has value less than zero.

@R1
D = M;

@R2
M = D + M;                     //Adding R1 to the temporary sum in R2.


@LOOP                         //Infinite loop.
0;JMP

(END)
@R2
M = M + 1;
