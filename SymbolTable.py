import Parser

NewMemory = 0

def table():
	global dictionary
	dictionary = {	
			'SP':0,
			'LCL':1,
			'ARG':2,
			'THIS':3,
			'THAT':4,
			'SCREEN':16384,
			'KBD':24576,
			'R0':0,
			'R1':1,
			'R2':2,
			'R3':3,
			'R4':4,
			'R5':5,
			'R6':6, 
			'R7':7,
            		'R8':8, 
			'R9':9, 
			'R10':10, 
			'R11':11, 
			'R12':12, 
			'R13':13, 
			'R14':14,
			'R15':15
		     }
	
def contains(sym):
	if sym in dictionary:
		return 1
	else: return 0

def addEntryLabel(sym,commandNumber):
	dictionary[sym] = commandNumber
	
def addEntry(sym):
	global NewMemory
	dictionary[sym] = NewMemory
	NewMemory = NewMemory + 1
	
def getAddress(sym):
	return dictionary[sym]
