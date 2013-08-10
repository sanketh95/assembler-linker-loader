'''
	import regex module
'''
import re


'''
This class checks for lex and syntactic errors in the code
'''
class syntaxCheck:
	def __init__(self,code,parent):
		self.code=code
		self.loadAddress=0
		self.parent=parent
		self.lines=code.split('\n')
		self.lineCount=0
		self.opcodelist = []
		self.opcode_args = []
		self.opcode_size = []
		self.global_vars = {}
		self.sym_table_dict = {}
		self.files = []
		self.sym_tables = []
		self.args_dict_list = []
		self.length_dict_list = []
		self.var_dict = {}
		self.macros = []
		self.macro_dict = {}
		self.checkValid(self.lines)
		self.line_counter = int('C000',16)
		self.loadOpCode()
		self.loadFiles()
		self.updatesymbol_table()
		self.load(self.loadAddress)

		
	'''*****************************************************************************************************************************
		takes array of lines of assembly language code as input and checks if the code is valid
		if valid returns True
		else returns false
	'''	

	def loadFiles(self):
		text = self.code.split('\n')
		num = int(str(text[0]))
		for i in range(num):
			j=i+1
			t = str(text[j])
			self.assemble(t)
		self.loadAddress = str(text[len(text)-1])


	def gen_code(self,filename,args):

	    input_file = open((filename + '.txt'),'r')
	    input = input_file.read()
	    lines=input.split("\n")			
	    words=lines[0].split(" ")
	    length=len(words)
	    str = ''
	    for i in range(len(lines) - 1):
	        str = str + lines[i+1] + '\n'
	    for i in range(len(args)):        
	        if(str.find(words[i])!=-1):
	            str=str.replace(words[i],args[i])
	            #print str
	    return str


	def updatesymbol_table(self) :
		
		addr = self.line_counter
		for key in self.var_dict:
			self.var_dict[key] = addr
			addr = addr + 1
		for key in self.global_vars:
			self.global_vars[key] = addr
			addr = addr + 1
		self.line_counter = addr
		print "VAR_table Dictionary : %s" %  str(self.var_dict)	
		print "Global table dictionary : %s" % str(self.global_vars)

    
	def loadOpCode(self):
    	
		# This loads opcode to table.
		file = open('opcode.txt','r')
		for line in file:
			words=line.split('\t')
			self.opcodelist.append(words[0])
			self.opcode_args.append(int(words[1]))
			self.opcode_size.append(int(words[2]))
		file.close()
		
		pass

	def expand(self,macro,args):

	    tup = self.macro_dict[macro]
	    parameters = tup[1]
	    macrodef = tup[2]
	    
	    s = macrodef
	    for parameter, arg in zip(parameters, args):
	        s = s.replace(parameter, arg)
	    return s

	def checkValid(self,lineArray):


		f = open('temp.txt','w')
		t = ''
		temp = ''
		for line in lineArray:
			if '//' in line:
				line = line.split('//')
				line = line[0]
			#print line
			if line != '':	
				literals = self.lineParse(line)
				#print literals
				if len(literals) != 0:
					literals = literals[0]
					for l in literals:
						if l != '':
							temp= temp + l + ' '
					t = t + temp + '\n'
					temp = ''
					if len(literals) != 0:
						if not self.validLiterals(literals):
							pass
						else:
							pass
					else:
						print('synax error')
		f.writelines(t)
		return True
			
	'''************************************************************************************************************************

		Takes a string as input and returns the list of words in the string
		uses regular expressions
	'''
	def lineParse(self,line):
		pattern="^\s*([a-zA-Z0-9]+:)\s*|([a-zA-Z]+)\s*([a-zA-Z0-9]+)?\s*,?\s*([a-zA-Z0-9]+)?\s*"
		m=re.findall(pattern,line)
		print m
		'''
			m should contain a list of literals
		'''
		return m
		

		'''*********************************************************************************************************************
				isValidInstruction(self,instruction) takes in instruction as parameter 
				and checks if the passed value is a valid instruction
		'''

		

	'''******************************************************************************************************************************
		takes the array of words returned by lineParse and checks if they are valid i.e, agree with the syntax of assembly language
	'''
	def validLiterals(self,lits):
		pass
	def load(self,addr):
		addr = int(addr,16)
		if len(self.files) > 0:
			for self.sym_dict in self.sym_tables:
				for key in self.sym_dict:
					address = int(self.sym_dict[key])
					address = address + addr
					self.sym_dict[key] = address

	#		print(sym_tables)

			output = ''
			for filename in self.files:
	#			print(filename)
				curr_index = self.files.index(filename)
				curr_args_dict = self.args_dict_list[curr_index]
	#			curr_sym_table_dict = sym_tables[curr_index]
				curr_len_dict = self.length_dict_list[curr_index]
				print "Symbol_table Dictionary : %s" %  str(self.sym_table_dict)	

				temp = ''
				f = open(filename.rstrip('.txt') + '_temp.txt','r')
				c = f.read()
				f.close()
				lines = c.split('\n')
				for line in lines:
					if line != '':

						if line.startswith('//'):
							continue
						words = line.split(' ')
						
	#					print(words)
						if(words[0].endswith(':')):
							continue
						for opcode in self.opcodelist:
							if(words[0] == opcode):
								if(opcode == 'DS'):
									break
								instr = ''
								instr_list = []
								for i in range(curr_args_dict[opcode] + 1):
									if (self.sym_table_dict.has_key(words[i])):
										instr = instr  + (hex(self.sym_table_dict[words[i]]).lstrip('0x')).upper() + ','
										instr_list.append((hex(self.sym_table_dict[words[i]]).lstrip('0x')).upper())
									elif (self.var_dict.has_key(words[i])):
										print 'in else if part'
										instr = instr + (hex(self.var_dict[words[i]]).lstrip('0x')).upper() + ','
										instr_list.append((hex(self.var_dict[words[i]]).lstrip('0x')).upper())		
									elif (self.global_vars.has_key(words[i])):
										print 'if global'
										instr = instr + (hex(self.global_vars[words[i]]).lstrip('0x')).upper() + ','
										instr_list.append((hex(self.global_vars[words[i]]).lstrip('0x')).upper())
									else:
										instr = instr + words[i] + ' '
										instr_list.append(words[i])
								temp = temp + self.gen_code(words[0], instr_list[1:])
						temp = temp.rstrip()
						temp = temp.rstrip(',')
						temp = temp + '\n'
				output = output+temp
				
			print(output)
		out = open('output.txt', 'w')
		out.writelines(output)
		out.close()




	def assemble(self,filename):
		self.files.append(filename);
	#	print(line_counter)
		args_dict = {}
		length_dict = {}


		args_dict = args_dict.fromkeys(self.opcodelist)
		for opcode, args in zip(self.opcodelist, self.opcode_args):
		#print 'opcode: {0}  #arguments: {1}.'.format(q, a)
			args_dict[opcode] = args
	#	print "arguments Dictionary : %s" %  str(args_dict)    

		# create dictionary for length

		length_dict = length_dict.fromkeys(self.opcodelist)
		for opcode, length in zip(self.opcodelist, self.opcode_size):
		#print 'opcode: {0}  #arguments: {1}.'.format(q, a)
			length_dict[opcode] = length
	#	print "length Dictionary : %s" %  str(length_dict)

		input_file = open(filename,'r')
		input = input_file.read()
		input_file.close()
		#This function checks for lexical errors
		# need to quit based on value

		lines = input.split('\n')
		# this loop is to find the start instruction
		inmacro = 'false'
		for line in lines:
		    if (line.startswith('//')):
		            continue
		    words = line.split(' ')

		    if(inmacro == 'true'):
		    	if (line != 'END'):
		    		macrodef = macrodef + '\n' + line
		    		lenght = lenght + length_dict[words[0]]
		    		print "macro Dictionary : %s" %  str(self.macro_dict)
		    	else :
		    		inmacro = 'false'
		    		macrodef = macrodef + '\n'
		    		self.macro_dict[macroname] = (macroname,parameters,macrodef,lenght)
		    if(words[0] == 'DEFINE'):
		    	self.macros.append(words[1])
		    	macroname = words[1]
		    	inmacro = 'true'
		    	macrodef = ''
		    	lenght = 0
		    	parameters = words[2:]

		    if(words[0] == 'START'):
		            self.line_counter = int(words[1],16)
	#	print type(line_counter)     
		output = ''            
		inmacro = 'false'            
		for line in lines:
		#line_counter = line_counter + 1
	#		print line_counter
			if (line.startswith('//')):
				continue
			words = line.split(' ')
			print words
			if(words[0] == 'DEFINE'):
				inmacro = 'true'
				continue
			if(inmacro == 'true'):
				if (words[0] == 'END'):
					inmacro = 'false'
				continue	
			print self.macros	
			for macro in self.macros:
				if (words[0] == macro):
					print('kjhdkj')
					s = self.expand(macro,words[1:])
					#print s
					output = output + s	
					#print lines
					#inmacro = 'true'
					print(macro)				

			if(words[0].endswith(':')):
				# means it is label
					self.sym_table_dict[words[0].rstrip(':')] = self.line_counter
					output = output + line
					continue
			if(words[0] == 'ENTRY'):
				
				self.global_vars[words[1]] = -1
			for opcode in self.opcodelist:
				if(words[0] == opcode):
					# means it is instruction
					if(opcode == 'DS'):
						self.var_dict[words[1]] = -1
					self.line_counter = self.line_counter + length_dict[opcode]
					output = output + line
			output = output.rstrip()
			output = output.rstrip(',')
			output = output + '\n'
			
		out = open(filename.rstrip('.txt') + '_temp.txt', 'w')
		out.writelines(output)
		out.close()

		self.args_dict_list.append(args_dict)
		self.length_dict_list.append(length_dict)
		# this correspondes to second pass algorithm

		input_file = open(filename.rstrip('.txt') + '_temp.txt','r')
		input = input_file.read()
		input_file.close()
		lines = input.split('\n')
		output = ''
		for line in lines:
			if (line.startswith('//')):
				# means comment
				continue
			words = line.split(' ')
			if(words[0].endswith(':')):
				# means it is label
				continue
			for opcode in self.opcodelist:
				if(words[0] == opcode):
					# it means opcode
					#output = output + opcode + ' '
					if(opcode == 'DS'):
						break
					instr = ''
					instr_list = []
					for i in range(args_dict[opcode] + 1):
						if (self.sym_table_dict.has_key(words[i])):
	#						print 'in if part'
							instr = instr + (hex(self.sym_table_dict[words[i]]).lstrip('0x')).upper() + ','
							instr_list.append((hex(self.sym_table_dict[words[i]]).lstrip('0x')).upper())
						elif (self.var_dict.has_key(words[i])):
		#					print 'in else if part'
	#						instr = instr + (hex(var_dict[words[i]]).lstrip('0x')).upper() + ','
	#						instr_list.append((hex(var_dict[words[i]]).lstrip('0x')).upper())	
							pass
						else:
							instr = instr + words[i] + ' '
							instr_list.append(words[i])
					output = output + self.gen_code(words[0], instr_list[1:])
			output = output.rstrip()
			output = output.rstrip(',')
			output = output + '\n'

	#	print output
		out = open(filename.split('.')[0]+'_output.txt', 'w')
		out.writelines(output)
		out.close()

	

'''

Function called while loading
'''



'''********************************************************************************************
The table
'''		
class literalTable(dict):
	def __init__(self):
		super(literalTable,self).__init__()

'''***************************************************************************************************
this class holds the assembled code in an array of lines (*-*) \m/ _/\_

'''
class assembledCode:
	def __init__(self):
		pass 
		
		
		