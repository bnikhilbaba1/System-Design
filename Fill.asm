// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

(AGAIN)                                              

@SCREEN           
D = A;
@COUNTER                                             
M = D;

@KBD                                                 
D = M;
@BLACKSCREEN
D;JNE
@WHITESCREEN
D;JEQ

(BLACKSCREEN)
@R1
D = -1;
@ASSIGN
0;JMP


(WHITESCREEN)
@R1
D = 0;

(ASSIGN)
@COLOUR                                         
M = D;

(LOOP)

@COLOUR
D = M;

@COUNTER
A = M;
M = D;

@COUNTER
M = M + 1;
D = M; 

@24576
D = D - A;

@AGAIN
D;JGE

@LOOP
0;JMP


(END)
@END
0;JMP
