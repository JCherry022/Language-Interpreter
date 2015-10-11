#!/util/bin/python
#John Cherry - Language-Interpreter 
#Compile with python3 
import os.path


stack = []
func = []
namedict = dict()
closure = []

def repl():
	i = 0
	str = input("repl> ")
	while(str != "quit"):
		split(str)
		for item in stack:
			print(item)
	
		str = input("repl> ")
		i = i + 1		

def split(input):
	i = 0
	count = 0
	words = input.split()
	buildstring = ""
	buildfunc = ""
	checkstring = 0
	checkbrak = 0
	checkapply = 0
	openbrace = 0
	closebrace = 0
	quote = 0

	for word in words:	#iterates through the userinput 
		if words[i][0] == "-" and checkstring == 0: #if leading character is a - and follows with numbers converts to a negative number
			negs = words[i].lstrip('-')
			negs = -int(negs)
			stack.insert(0,negs)
	
		elif words[i][0] == '"' or checkstring == 1: #allowing strings to be entered into repl
			checkstring = 1
			if words[i][0] == '"' or words[i][-1] == '"':
				quote = quote + 1
				buildstring = buildstring + words[i]
				if len(words[i]) > 1 and words[i][0] == '"' and words[i][-1] == '"':
					quote = quote + 1
				if len(words[i]) > 1 and words[i][0] == '"' and words[i][-1] != '"':
					buildstring = buildstring + ' '
				if len(words[i]) == 1 and words[i][0] == '"':
					buildstring = buildstring + ' '
			elif '"' in words[i]:
				stack.insert(0,":error:")
				buildstring = ""
				quote = 0
				checkstring = 0
			else:
				buildstring = buildstring + words[i] + ' '
			if quote == 2:
				stack.insert(0, buildstring)
				buildstring = ""
				quote = 0
				checkstring = 0
				
		
		elif words[i][0] == "{" or checkbrak == 1: #allowing func to be put on stack
			checkbrak = 1
			if words[i] == '{':
				openbrace = openbrace + 1
			if words[i] == '}':
				closebrace = closebrace + 1
			if openbrace == closebrace and len(buildfunc) >= 4:
				buildfunc = buildfunc + '}'
				func.insert(0, buildfunc)
				stack.insert(0, ":closure:")
				buildfunc = ""
				checkbrak = 0
				closebrace = 0
				openbrace = 0
			elif i != len(words) - 1:
				buildfunc = buildfunc + words[i] + ' '
			else:
				stack.insert(0,":error:")
				buildfunc = ""
				checkbrak = 0
				closebrace = 0
				openbrace = 0

		elif words[i].isnumeric() and checkstring == 0: #checks to see if userinput is a number and inserts the number in to the stack
			num = int(words[i])
			stack.insert(0,num)

		elif words[i] == "add" and checkstring == 0:
			add()
		elif words[i] == ":true:" and checkstring == 0:
			stack.insert(0,":true:")
		elif words[i] == ":false:" and checkstring == 0: 
                        stack.insert(0,":false:")	
		elif words[i] == "sub" and checkstring == 0:
			sub()
		elif words[i] == "mul" and checkstring == 0:
			mul()
		elif words[i] == "div" and checkstring == 0:
			div()
		elif words[i] == "rem" and checkstring == 0:
			rem()
		elif words[i] == "neg" and checkstring == 0:
			neg()
		elif words[i] == "pop" and checkstring == 0:
			pop()
		elif words[i] == "exc" and checkstring == 0:
			exc()
		elif words[i] == "and" and checkstring == 0:
			an()
		elif words[i] == "or" and checkstring == 0:
			ori()
		elif words[i] == "not" and checkstring == 0:
			noti()
		elif words[i] == "equal" and checkstring == 0:
			equal()
		elif words[i] == "lessThan" and checkstring == 0:
			lessthan()
		elif words[i] == "load" and checkstring == 0:
			load()
		elif words[i] == "bind" and checkstring == 0:
			bind()
		elif words[i] == "if" and checkstring == 0:
			ify()
		elif words[i] == "length" and checkstring == 0:
			strlength()
		elif words[i] == "concat" and checkstring == 0:
			strconcat()
		elif words[i] == "[]" and checkstring == 0:
			listinstack()
		elif words[i] == "prepend" and checkstring == 0:
			prependlist()
		elif words[i] == "rest" and checkstring == 0:
			rest()
		elif words[i] == "first" and checkstring == 0:
			first()		
		elif words[i] == "apply":
#				print("top vault of stack:", stack[0])
				if stack[0] == ":closure:":
		#			print("top here", stack[0])
					stack.pop(0)
					if len(func[0]) == 5:
						function = func[0][2]
					else:
						function = func[0][2:-2]
			#		print("val func", function) 
					#func.pop(0)
					split(function)
				else:
					stack.insert(0,":error:")
				
		elif words[i][0].isalpha():  #allowing names to be inputed into the stack starting a letter followed by a sequence of characters  
			if words[i] in namedict:
#				print("ji the dict:", namedict)
				name = namedict[word]
				
#				print("ahhh the ",word ," holds value:", name)
			else:
				name = words[i]
				count = 0
#				print("nooo the dict holds:", namedict)

			schpairs(stack, name, name)
		else:
			stack.insert(0,":error:")
#		print("yeah dict holds now:", namedict)

#		print("func string:", func)

		i = i + 1
def first():
	if len(stack) >= 1:
		first = stack[0]
		if isinstance(first,int):
			stack.insert(0,":error:")
		elif len(first) == 0:
			stack.insert(0,":error:") 
		elif isinstance(first,list):
			posone = first[0]
			stack.insert(0,posone)
		else:
			stack.insert(0,":error:")
	else:
		stack.insert(0,":error:")	
def rest():
	if len(stack) >= 1:
		first = stack[0]
		if isinstance(first,int):
			stack.insert(0,":error:")
		elif len(first) == 0:
			stack.insert(0,":error:") 
		elif isinstance(first,list):
			lenlist = len(first)
			restlist = first[1:lenlist]
			stack.insert(0,restlist)
		else:
			stack.insert(0,":error:")
	else:
		stack.insert(0,":error:") 

def listinstack():
	stack.insert(0,[])

def prependlist():
	if len(stack) >= 1:
		first = stack[0]
		second = stack[1]
		stack.pop(0)
		second.insert(0,first)
	else:
		stack.insert(0,":error:")
def strconcat():
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if first[0][0] == "\"" and second[0][0] == "\"":
			first = stack[0][1:-2]
			second = stack[1][1:-2]
			concat = "\"" + second + first + "\""
			stack.pop(0)
			stack.pop(0)
			stack.insert(0,concat)
		else:
			stack.insert(0,":error:")

def strlength():
	if len(stack) >= 1:
		first = stack[0]
		if first[0][0] == "\"":
			first = stack[0][1:-2]
			length = len(first)
			stack.insert(0,length)
		else:
			stack.insert(0,":error:")

def schpairs(stack, local, notlocal):
	if isinstance(local,int):
		local = str(local)
	if isinstance(notlocal,int):
		notlocal = str(notlocal)
	spair = ""
	spair = '<' + local + ',' + notlocal + '>'
	stack.insert(0, spair)

def getLocal(scpair):
	local = ""
	i = 1
	while(scpair[i] != ','):
		local = local + scpair[i]
		i = i + 1
	return local

def getnotlocal(scpair):
	notlocal = ""
	i = 1
	while(scpair[i] != ','):
		i = i + 1
	i = i + 1
	while(scpair[i] != '>'):
		notlocal = notlocal + scpair[i]
		i = i + 1
	return notlocal

def load():
	if len(stack) >= 1:
		first = stack[0]
		if first[0][0] == "\"":
			first = stack[0][1:-2]
			if os.path.isfile(first):
				stack.insert(0,":true:")
			else:
				stack.insert(0,":false:")
	else:
		stack.insert(0,":error:")

def ify():
	if len(stack) > 2:	
		first = stack[0]
		second = stack[1]
		third = stack[2]
		if first == ":true:":
			stack.pop(0)
			stack.pop(0)
			stack.pop(0)
			stack.insert(0, third)
		elif first == ":false:":
			stack.pop(0)
			stack.pop(0)
			stack.pop(0)
			stack.insert(0, second)
		else:
			stack.insert(0, ":error:")	
	else:
		stack.insert(0, ":error:")

def bind():
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if isinstance(second,int):	# check to see if second is a number bc you cant bind to numbers
			stack.insert(0,":error:")	
		elif second[0][0].isalpha():    # check first char to see if its a name
			stack.pop(0)
			stack.pop(0)
			namedict[second] = first # = namedict.get(first, second) # Add new entry in dictionary
			stack.insert(0,first)
		elif second[0] == '<':
			local = getLocal(second)
			if( (not local.isdigit()) and local[0].isalpha):
				stack.pop(0)
				stack.pop(0)
				if not isinstance(first,int) and first[0] == '<':
					notlocal = getnotlocal(first)
				else:
					notlocal = first
				namedict[local] = notlocal
				stack.insert(0,notlocal)
			else:
				stack.insert(0,":error:")
							
		else:
			stack.insert(0,":error:")
	else:
		stack.insert(0,":error:")
 
def lessthan():
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]

		if not isinstance(first, int) and first[0] == '<':
			first = getnotlocal(first)
			first = int(first)
		if not isinstance(second, int) and second[0] == '<':
			second = getnotlocal(second)
			second = int(second)		

		if isinstance(second,int) and isinstance(first,int):
			if second < first:
				stack.pop(0)
				stack.pop(0)
				stack.insert(0,":true:")
			else:
				stack.pop(0)
				stack.pop(0)
				stack.insert(0,":false:")
		else:
			stack.insert(0,":error:")
	else:
		stack.insert(0,":error:")

def equal():
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if not isinstance(first, int) and first[0] == '<':
			first = getnotlocal(first)
			first = int(first)
		if not isinstance(second, int) and second[0] == '<':
			second = getnotlocal(second)
			second = int(second)

		if second and first:
			if first == second:
				stack.pop(0)
				stack.pop(0)
				stack.insert(0,":true:")
			else:
				stack.pop(0)
				stack.pop(0)
				stack.insert(0,":false:")

def noti():
	if len(stack) >= 1:
		first = stack[0]
		if (first != ":true:" or first != ":false:"):
			stack.insert(0,":error:")		
		
		if (first == ":true:"):
			stack.pop(0)
			stack.pop(0)
			stack.insert(0,":false:")
		if (first == ":false:"):
			stack.pop(0)
			stack.pop(0)
			stack.insert(0,":true:")

def ori():
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if (first != ":true:" or first != ":false:") and (second != ":true:" or second != ":false:"):
               		stack.insert(0,":error:")

		if (first == ":true:" and  second == ":true:"):
			stack.pop(0)
			stack.pop(0)
			stack.pop(0)
			stack.insert(0,":true:")
		
		if (first == ":false:" and second == ":false:"):
			stack.pop(0)
			stack.pop(0)
			stack.pop(0)
			stack.insert(0,":false:")
		if (first == ":true:" and second == ":false:") or (first == ":false:" and second == ":true:"):
			stack.pop(0)
			stack.pop(0)
			stack.pop(0)
			stack.insert(0,":true:")

	else:
                stack.insert(0,":error:")

def an():
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if (first != ":true:" and first != ":false:") or (second != ":true:" and second != ":false:"):
			stack.insert(0,":error:")
		
		if (first == ":true:" and second == ":true:"):
			stack.pop(0)
			stack.pop(0)
			stack.insert(0,":true:")
		if (first == ":false:" and second == ":true:") or (first == ":true:" and second == ":false:"):
                	stack.pop(0)
                	stack.pop(0)
                	stack.insert(0,":false:")
		if (first == ":false:" and second == ":false:"):
			stack.pop(0)
			stack.pop(0)
			stack.insert(0,":false:")
	
	else: 
		stack.insert(0,":error:")

def add():
	added = 0
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if not isinstance(first, int) and first[0] == '<':
			first = getnotlocal(first)
			first = int(first)
		if not isinstance(second, int) and second[0] == '<':
			second = getnotlocal(second)
			second = int(second)
		if isinstance(first,int) and isinstance(second,int):
			stack.pop(0)
			stack.pop(0)
			added = int(second) + int(first)
			added = int(added)
			stack.insert(0,added)
		
		else:
			stack.insert(0,":error")
	else:
		stack.insert(0,":error:")

def sub():
	subbed = 0
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if not isinstance(first, int) and first[0] == '<':
			first = getnotlocal(first)
			first = int(first)
		if not isinstance(second, int) and second[0] == '<':
			second = getnotlocal(second)
			second = int(second)

		if isinstance(first,int) and isinstance(second,int):
			stack.pop(0)
			stack.pop(0)
			subbed = int(second) - int(first)
			subbed = int(subbed)
			stack.insert(0,subbed)
		else:
			stack.insert(0,":error:")
	else:

		stack.insert(0,":error:")

def mul():
	multi = 0
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if not isinstance(first, int) and first[0] == '<':
			first = getnotlocal(first)
			first = int(first)
		if not isinstance(second, int) and second[0] == '<':
			second = getnotlocal(second)
			second = int(second)

		if isinstance(first,int) and isinstance(second,int):
			stack.pop(0)
			stack.pop(0)
			multi = int(second) * int(first)
			multi = int(multi)
			stack.insert(0,multi)
		else:
			stack.insert(0,":error:")
	else:
		stack.insert(0,":error:")

def div():
	divided = 0
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		
		if not isinstance(first, int) and first[0] == '<':
			first = getnotlocal(first)
			first = int(first)
		if not isinstance(second, int) and second[0] == '<':
			second = getnotlocal(second)
			second = int(second)
		if int(first) == 0:
			stack.insert(0,":error:")
		elif isinstance(first,int) and isinstance(second,int):
			stack.pop(0)
			stack.pop(0)
			divided = int(second) / int(first)
			divided = int(divided)
			stack.insert(0,divided)
		else:
			stack.insert(0,":error")		
	else:
		stack.insert(0,":error:")

def rem():
	rem = 0
	if len(stack) > 1:
		first = stack[0]
		second = stack[1]
		if not isinstance(first, int) and first[0] == '<':
			first = getnotlocal(first)
			first = int(first)
		if not isinstance(second, int) and second[0] == '<':
			second = getnotlocal(second)
			second = int(second)
		if isinstance(first,int) and isinstance(second,int):
			stack.pop(0)
			stack.pop(0)
			rem = int(second) % int(first)
			rem = int(rem)
			stack.insert(0,rem)
		else:
			stack.insert(0,":error:")
	else:
		stack.insert(0,":error:")

def neg():
	if len(stack) >= 1:
		first = stack[0]
		if not isinstance(first, int) and first[0] == '<':
			first = getnotlocal(first)
			first = int(first)
		if isinstance(first,int):
			stack.pop(0)
			first = -int(first) 
			stack.insert(0,first)
		else:
			stack.insert(0,":error:")
	else:
		stack.insert(0,":error:")

def pop():
	if not stack: #if stack is empty insert error
		stack.insert(0,":error:")
		return 0	

	stack.pop(0)
	
def exc():
	if not stack: #if stack is empty insert error
		stack.insert(0,":error:")
		return 0
	num = stack[0]
	if not stack: #if stack only has one int insert error
		stack.insert(0,num)
		stack.insert(0,":error:")
		return 0 
	top = stack.pop(0)
	next = stack.pop(0)
	stack.insert(0,top)
	stack.insert(0,next)
	
repl()
