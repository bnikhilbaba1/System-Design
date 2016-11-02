
#Parser function
def parser():
	global inputfile,Lines
	inputfile = open("Max.asm","r")
	Lines = inputfile.readlines()  #Opening and reading all the lines in the input(Storing them in an array)



#Progresses to the given line
def ShowLine(i):
	return Lines[i]



#Returns number of lines	
def size():
	n =len(Lines)
	return n

#Detects the type of command the given command is...
def commandType(line):
	i = 0
	size = len(line)
	if(size == 0):
		return 0
	while(i < size):
		if(line[i] == '/' and line[i + 1] == '/'): 
			break #The line is a comment
		if(line[i] == '('):                        
			return "L_command"
		if(line[i] == '@'):
			return "A_command"
		if(line[i] == ';' or line[i] == '='):
			return "C_command"
		i = i + 1 #Returning type of command of all commands
	return 0

def NewVariable(line):
	i = 0
	size = len(line)
	if(commandType(line) == "L_command"):
		while(i < size):	
			if(line[i] == '/' and line[i+1] == '/'): 
				break              #Checking whether it is a comment or not                   
			if(line[i] == '('):
				start = i+1
			if(line[i] == ')'): 
				end = i
				break
			i = i + 1
		line = line[start:end]  #Shorten the length of variable to that name
		return line
	i = 0
	if(commandType(line) == "A_command"):
		line = line.strip()
	#	line = line.strip('	') Shortening the command
		line = line.replace(' ','')
		line = line.replace('	','')
		if '//' in line:
			return line[line.index('@')+1 : line.index('//')] #Shortening the length of the line to omit comments(if there are any)
		else: 
			return line[line.index('@')+1 :]#To return string if there are no comments

def Destination(line):
	line = line.strip()
	line = line.replace(' ','')
	line = line.replace('	','')
	if '=' in line:
		return line[:line.index('=')]
	else: return 'null'

def Source(line):
	line = line.strip()
	line = line.replace(' ','')
	line = line.replace('	','') #Shortening the command
	if ';' in line: #If  semicolon is used
		if '=' in line: 
			return line[line.index('=')+1 : line.index(';')]
		else: 
			return line[:line.index(';')]
	else:
		if '//' in line:#If semicolon is used,the last useful character is before //
			return line[line.index('=')+1 : line.index('//')]
		else: 
			return line[line.index('=')+1 :]

def JumpDestination(line):
	line = line.strip()
	line = line.replace(' ','')
	line = line.replace('	','')
	if ';' in line:
		if '//' in line:
			return line[line.index(';')+1 : line.index('//')]
		else: 
			return line[line.index(';')+1 :]
	else: 
		return 'null'
