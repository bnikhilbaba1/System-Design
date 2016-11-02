import sys
import os
import glob

segment_dict = { 'local' : 'LCL', 'argument' : 'ARG', 'this' : 'THIS', 'that' : 'THAT'}
static_vars = {}
count = 0

def convert_push_segment(segment, index, vm_filename):
	if segment == 'static':
		return "@" + (vm_filename).replace("vm", str(index)) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
	elif segment == 'constant':
		return "@" + str(index) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"	
	elif segment == 'pointer':
		if index == '0':
			return "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
		else:
			return "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
	elif segment == 'temp':
		return "@5\nD=A\n@" + str(index) + "\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
	else:
		return "@" + segment_dict[segment] + "\nD=M\n@" + str(index) + "\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"



def convert_pop_segment(segment, index, vm_filename):
	if segment == 'static':
		return "@SP\nM=M-1\nA=M\nD=M\n@" + (vm_filename).replace("vm", str(index)) + "\nM=D\n"
	elif segment == 'pointer':
		if index == '0':
			return "@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n"
		else:
			return "@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"
	elif segment == 'temp':
		return "@5\nD=A\n@" + str(index) + "\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
	else:
		return "@" + segment_dict[segment] + "\nD=M\n@" + str(index) + "\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"




def convert_operation(operation):
	global count
	if operation == 'add':
		return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M+D\n"
	elif operation == 'sub':
		return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\n"
	elif operation == 'and':
		return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M&D\n"
	elif operation == 'or':
		return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M|D\n"
	elif operation == 'neg':
		return "@SP\nA=M-1\nM=-M"
	elif operation == 'not':
		return "@SP\nA=M-1\nM=!M"
	elif operation == 'gt':
		count = count + 1
		return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@compare" + str(count) + "\nD;JGT\n@SP\nA=M-1\nM=0\n@end" + str(count) + "\n0;JMP\n(compare" + str(count) + ")\n@SP\nA=M-1\nM=-1\n(end" + str(count) + ")\n"
	elif operation == 'lt':
		count = count + 1
		return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@compare" + str(count) + "\nD;JLT\n@SP\nA=M-1\nM=0\n@end" + str(count) + "\n0;JMP\n(compare" + str(count) + ")\n@SP\nA=M-1\nM=-1\n(end" + str(count) + ")\n"
	elif operation == 'eq':
		count = count + 1
		return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@compare" + str(count) + "\nD;JEQ\n@SP\nA=M-1\nM=0\n@end" + str(count) + "\n0;JMP\n(compare" + str(count) + ")\n@SP\nA=M-1\nM=-1\n(end" + str(count) + ")\n"


def convert_function(function_name, lcl_vars):
	asm_code = "(" + function_name +")\n"
	for i in range(int(lcl_vars)):
		asm_code = asm_code + convert_push_segment('constant', 0, "")
	return asm_code


def convert_call(function_name, args, line_no):
	pushing_return_address =  "@" + function_name + str(line_no) + "return\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
	pushing_lcl =  "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
	pushing_arg =  "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
	pushing_this =  "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
	pushing_that =  "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
	repositioning_arg = "@SP\nD=M\n@" + str(int(args)+5) + "\nD=D-A\n@ARG\nM=D\n"
	repositioning_lcl = "@SP\nD=M\n@LCL\nM=D\n"
	going_to_function = "@" + function_name +"\n0;JMP\n"
	declaring_return = "(" + function_name + str(line_no) + "return)\n"
	return pushing_return_address + pushing_lcl + pushing_arg + pushing_this + pushing_that + repositioning_arg + repositioning_lcl + going_to_function + declaring_return


def convert_return():
	frame_equals_lcl = "@LCL\nD=M\n@frame\nM=D\n"
	store_return = "@frame\nD=M\n@5\nA=D-A\nD=M\n@return_add\nM=D\n"
	repositioning_return_value = "@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n"
	repositioning_sp = "@ARG\nD=M+1\n@SP\nM=D\n"
	repositioning_that = "@frame\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"
	repositioning_this = "@frame\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n"
	repositioning_arg = "@frame\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n"
	repositioning_local = "@frame\nM=M-1\nA=M\nD=M\n\n@LCL\nM=D\n"
	going_to_return = "@return_add\nA=M\n0;JMP\n"
	return frame_equals_lcl + store_return + repositioning_return_value + repositioning_sp + repositioning_that + repositioning_this + repositioning_arg + repositioning_local + going_to_return




asm_file = open((sys.argv[1] + "/" + sys.argv[1] + ".asm"), "w")
current_function_list = []

vm_dir = os.listdir(sys.argv[1])
line_no = 0

asm_file.write("@256\nD=A\n@SP\nM=D\n")
if "Sys.vm" in vm_dir:
	asm_file.write(convert_call('Sys.init', '0', 1 ) + '\n')
	line_no = 2;


for vm_filename in vm_dir:
	if vm_filename.endswith('.vm'):
		vm_file = open(sys.argv[1] + '/' + vm_filename)
		#print(vm_filename)
		for line in vm_file:
			if len(line.strip()) > 0 and line.strip()[0] != chr(47):
				line_no +=1
				if line.strip()[0:4] == 'push':
					(push, segment, index) = line.strip().split(chr(47))[0].strip().split(' ')
					asm_code = convert_push_segment(segment.strip(), index.strip(), vm_filename)
				elif line.strip()[0:3] == 'pop':
					(pop, segment, index) = line.strip().split(chr(47))[0].strip().split(' ')
					asm_code = convert_pop_segment(segment.strip(), index.strip(), vm_filename)
				elif line.strip()[0:5] == 'label':
					(label, label_name) = line.strip().split(chr(47))[0].strip().split(' ')
					asm_code = '(' + label_name + ')\n'
				elif line.strip()[0:4] == 'goto':
					(goto, label_name) = line.strip().split(chr(47))[0].strip().split(' ')
					asm_code = '@' + label_name + '\n0;JMP\n'
				elif line.strip()[0:7] == 'if-goto':
					(if_goto, label_name) = line.strip().split(chr(47))[0].strip().split(' ')
					asm_code = '@SP\nM=M-1\n@SP\nA=M\nD=M\n@' + label_name + '\nD;JNE\n'
				elif line.strip()[0:8] == 'function':
					(function, function_name, lcl_vars) = line.strip().split(chr(47))[0].strip().split(' ')
					asm_code = convert_function(function_name, lcl_vars)
					current_function_list.append(function_name)
				elif line.strip()[0:4] == 'call':
					(call, function_name, args) = line.strip().split(chr(47))[0].strip().split(' ')
					asm_code = convert_call(function_name, args, line_no)
				elif line.strip()[0:6] == 'return':
					asm_code = convert_return()			
				else:
					asm_code = convert_operation(line.strip().split(chr(47))[0].strip())
				asm_file.write(asm_code + "\n")

		

