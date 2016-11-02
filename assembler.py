import Parser
import Code
import SymbolTable

Parser.parser()
SymbolTable.table()
Code.code()
length = Parser.size()
commandNumber = 0
i = 0

while(i < length):
	line = Parser.ShowLine(i)
	if (Parser.commandType(line) == 0):
		i = i + 1
		continue
	if(Parser.commandType(line) == "A_command"): 
		commandNumber = commandNumber + 1
	if(Parser.commandType(line) == "C_command"): 
		commandNumber = commandNumber + 1
	if (Parser.commandType(line) == "L_command"):
		sym = Parser.NewVariable(line)
		if (SymbolTable.contains(sym) == 0):
			SymbolTable.addEntryLabel(sym,commandNumber)
	i = i + 1



#First pass of the assembler
i = 0

while(i < length):
	line = Parser.ShowLine(i)
	if (Parser.commandType(line) == 0):#Not a command
		i = i + 1
		continue
	if (Parser.commandType(line) == "A_command"):
		sym = Parser.NewVariable(line)
		if(sym.isdigit()):
			i = i + 1
			continue
		if (SymbolTable.contains(sym) == 0):
			SymbolTable.addEntry(sym)
	i = i + 1


#Second pass of the assembler
i = 0

#Opening of the output file
outputfile = open('Rect.hack','w')

while(i < length):
	line = Parser.ShowLine(i)
	if(Parser.commandType(line) == "A_command"):
		sym = Parser.NewVariable(line)
		if(sym.isdigit()):
			x = bin(int(sym))
			x = int(x[2:])
			outputfile.write(format(x,"016d"))
			outputfile.write("\n")
		else:
			x = SymbolTable.getAddress(sym)
			x = bin(int(x))
			x = int(x[2:])
			outputfile.write(format(x, "016d"))
			outputfile.write("\n")
	if(Parser.commandType(line) == "C_command"):
		symcomp = Parser.Source(line)
		bincomp = Code.Operation(symcomp)
		symdest = Parser.Destination(line)
		bindest = Code.Destination(symdest)
		symjump = Parser.JumpDestination(line)
		binjump = Code.JumpDestination(symjump)
		x = "111" + bincomp + bindest + binjump
		outputfile.write(x)
		outputfile.write("\n")
	i = i + 1
