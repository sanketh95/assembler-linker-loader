# these are global variables
opcodelist = []
opcode_args = []
opcode_size = []
global_vars = {}
sym_table_dict = {}
files = []
sym_tables = []
args_dict_list = []
length_dict_list = []
var_dict = {}
macros = []
macro_dict = {}

def checkinput():
	return 1


def gen_code(filename,args):

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

def loadOpCode():
	# This loads opcode to table.
	file = open('opcode.txt','r')
	for line in file:
		words=line.split('\t')
		opcodelist.append(words[0])
		opcode_args.append(int(words[1]))
		opcode_size.append(int(words[2]))
	file.close()

def expand(macro,args):
    print 'in expand'
    tup = macro_dict[macro]
    parameters = tup[1]
    macrodef = tup[2]
    
    s = macrodef
    print s
    for parameter, arg in zip(parameters, args):
        s = s.replace(parameter, arg)
    return s   

def checkinput(input):
	return 1;

# create dictionary for number of arguments
def assemble(filename):
	files.append(filename);
	global line_counter
#	print(line_counter)
	args_dict = {}
	length_dict = {}


	args_dict = args_dict.fromkeys(opcodelist)
	for opcode, args in zip(opcodelist, opcode_args):
	#print 'opcode: {0}  #arguments: {1}.'.format(q, a)
		args_dict[opcode] = args
#	print "arguments Dictionary : %s" %  str(args_dict)    

	# create dictionary for length

	length_dict = length_dict.fromkeys(opcodelist)
	for opcode, length in zip(opcodelist, opcode_size):
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
	line_counter = int('C000',16)
	inmacro = 'false'
	for line in lines:
	    if (line.startswith('//')):
	            continue
	    words = line.split(' ')

	    if(inmacro == 'true'):
	    	if (line != 'END'):
	    		macrodef = macrodef + '\n' + line
	    		print "macro Dictionary : %s" %  str(macro_dict)
	    	else :
	    		inmacro = 'false'
	    		macrodef = macrodef + '\n'
	    		macro_dict[macroname] = (macroname,parameters,macrodef)    
	    if(words[0] == 'DEFINE'):
	    	macros.append(words[1])
	    	macroname = words[1]
	    	inmacro = 'true'
	    	macrodef = ''
	    	parameters = words[2:]

	    if(words[0] == 'START'):
	            line_counter = int(words[1],16)
#	print type(line_counter)     
	output = ''            
	inmacro = 'false'            
	for line in lines:
	#line_counter = line_counter + 1
#		print line_counter
		if (line.startswith('//')):
			continue
		words = line.split(' ')
		#print words
		for macro in macros:
			if (words[0] == macro):
				s = expand(macro,words[1:])
				#print s
				output = output + s	
				#print lines
				#inmacro = 'true'
				continue
		if(words[0] == 'DEFINE'):
			inmacro = 'true'		
		if(inmacro == 'true'):
			if (words[0] == 'END'):
				inmacro = 'false'
			continue	

		if(words[0].endswith(':')):
			# means it is label
				sym_table_dict[words[0].rstrip(':')] = line_counter
				output = output + line
				continue
		if(words[0] == 'ENTRY'):
			
			global_vars[words[1]] = -1
		for opcode in opcodelist:
			if(words[0] == opcode):
				# means it is instruction
				if(opcode == 'DS'):
					var_dict[words[1]] = -1
				line_counter = line_counter + length_dict[opcode]
				output = output + line
		output = output.rstrip()
		output = output.rstrip(',')
		output = output + '\n'
		
	out = open(filename.rstrip('.txt') + '_temp.txt', 'w')
	out.writelines(output)
	out.close()

	args_dict_list.append(args_dict)
	length_dict_list.append(length_dict)
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
		for opcode in opcodelist:
			if(words[0] == opcode):
				# it means opcode
				#output = output + opcode + ' '
				if(opcode == 'DS'):
					break
				instr = ''
				instr_list = []
				for i in range(args_dict[opcode] + 1):
					if (sym_table_dict.has_key(words[i])):
#						print 'in if part'
						instr = instr + (hex(sym_table_dict[words[i]]).lstrip('0x')).upper() + ','
						instr_list.append((hex(sym_table_dict[words[i]]).lstrip('0x')).upper())
					elif (var_dict.has_key(words[i])):
	#					print 'in else if part'
#						instr = instr + (hex(var_dict[words[i]]).lstrip('0x')).upper() + ','
#						instr_list.append((hex(var_dict[words[i]]).lstrip('0x')).upper())	
						pass
					else:
						instr = instr + words[i] + ' '
						instr_list.append(words[i])
				output = output + gen_code(words[0], instr_list[1:])
		output = output.rstrip()
		output = output.rstrip(',')
		output = output + '\n'

#	print output
	out = open(filename.split('.')[0]+'_output.txt', 'w')
	out.writelines(output)
	out.close()

line_counter = int('0',16)
def test():
	print(line_counter)

'''

Function called while loading
'''

def updatesymbol_table():
	global line_counter
	addr = line_counter
	for key in var_dict:
		var_dict[key] = addr
		addr = addr + 1
	for key in global_vars:
		global_vars[key] = addr
		addr = addr + 1
	print "VAR_table Dictionary : %s" %  str(var_dict)	
	print "Global table dictionary : %s" % str(global_vars)

def load(addr):
	if len(files) > 0:
		for sym_dict in sym_tables:
			for key in sym_dict:
				address = int(sym_dict[key])
				address = address + addr
				sym_dict[key] = address

#		print(sym_tables)

		output = ''
		for filename in files:
#			print(filename)
			curr_index = files.index(filename)
			curr_args_dict = args_dict_list[curr_index]
#			curr_sym_table_dict = sym_tables[curr_index]
			curr_len_dict = length_dict_list[curr_index]
			print "Symbol_table Dictionary : %s" %  str(sym_table_dict)	

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
					for opcode in opcodelist:
						if(words[0] == opcode):
							if(opcode == 'DS'):
								break
							instr = ''
							instr_list = []
							for i in range(curr_args_dict[opcode] + 1):
								if (sym_table_dict.has_key(words[i])):
									instr = instr  + (hex(sym_table_dict[words[i]]).lstrip('0x')).upper() + ','
									instr_list.append((hex(sym_table_dict[words[i]]).lstrip('0x')).upper())
								elif (var_dict.has_key(words[i])):
									print 'in else if part'
									instr = instr + (hex(var_dict[words[i]]).lstrip('0x')).upper() + ','
									instr_list.append((hex(var_dict[words[i]]).lstrip('0x')).upper())		
								elif (global_vars.has_key(words[i])):
									print 'if global'
									instr = instr + (hex(global_vars[words[i]]).lstrip('0x')).upper() + ','
									instr_list.append((hex(global_vars[words[i]]).lstrip('0x')).upper())
								else:
									instr = instr + words[i] + ' '
									instr_list.append(words[i])
							temp = temp + gen_code(words[0], instr_list[1:])
					temp = temp.rstrip()
					temp = temp.rstrip(',')
					temp = temp + '\n'
			output = output+temp
			
		print(output)
	out = open('output.txt', 'w')
	out.writelines(output)
	out.close()
				

loadOpCode()
assemble('input.txt')
updatesymbol_table()
load(10)
