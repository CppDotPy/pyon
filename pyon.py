class private:

	# This class acts like a namespace
	# it holds classes that the end user
	# is not expected or supposed to use

	class block:
		def __init__(self, source):

			self.source = source
			self.block_start = 0
			self.parent = 'none'
			self.content = None
			self.child_indent = ''
			self.type = None
			self.variables = []
			self.lines = []

		def __repr__(self):

			line_data = []
			line_data.append(self.parent)
			line_data.append(self.type)
			line_data.append(self.child_indent)
			line_data.append(self.content)
			return f'{line_data}'

		def __add__(self, value): self.append(str(value))

		def write(self, string):

			problem = False
			if string != '' and len(string.split()) != 2: problem = True
			if string != '' and string[-1] != ':': problem = True
			if problem: raise SyntaxError('Write requires argument to declare a variable')

			source = self.source
			tail = ''
			head = ''
			block = string
			in_block = False
			lines = source.lines
			line_number = self.block_start
			for line in lines:
				construct = line.reconstruct() + '\n'
				if line.line_number == line_number: in_block = True
				if in_block and line.indent_level < self.child_indent and line.line_number != line_number: in_block = False
				if line.line_number < line_number and not in_block: head += construct
				if line.line_number > line_number and not in_block: tail += construct

			with open(source.source, 'w') as file:
				file.write(head)
				file.write(block)
				file.write(tail)

			with open(source.source, 'r') as file:
				source.lines = file.readlines()
			source.create_line_objects()
			source.assign_object_values()

		def append(self, string):

			if string == '': string = '\n'
			source = self.source
			tail = ''
			head = ''
			lines = source.lines
			line_number = self.block_start
			passed_end_of_block = False
			in_block = False

			for line in lines:
				construct = line.reconstruct() + '\n'
				if line.line_number == line_number: in_block = True
				if line.indent_level < self.child_indent and in_block and line.line_number != line_number:
					passed_end_of_block = True
					in_block = False
				if line.line_number <= line_number: head += construct
				if line.line_number > line_number:
					if passed_end_of_block: tail += construct
					else: head += construct

			leading_whitespace = '\t' * self.child_indent
			with open(source.source, 'w') as file:
				file.write(head)
				file.write(f'{leading_whitespace}{string}')
				file.write(tail)

			with open(source.source, 'r') as file:
				source.lines = file.readlines()
			source.create_line_objects()
			source.assign_object_values()

		def read(self): return self.variables

		def read_all(self): return self.lines

	class line:
		def __init__(self):

			self.line_number = 0
			self.indent_level = ''
			self.parent = 'none'
			self.parent_name = 'none'
			self.content = ''
			self.type = None
			self.is_assignment = False

		def __repr__(self):

			line_data = []
			line_data.append(self.parent_name)
			line_data.append(self.line_number)
			line_data.append(self.indent_level)
			line_data.append(self.is_assignment)
			line_data.append(self.type)
			line_data.append(self.parent)
			line_data.append(self.content)
			return f'{line_data}'

		def reconstruct(self):

			leading_whitespace = '\t' * self.indent_level
			if self.is_assignment: content = f'{leading_whitespace}{self.type} {self.content}:'
			else: content = f'{leading_whitespace}{self.content}'
			return content

class pyon:

	block = private.block
	line = private.line

	def __init__(self, source):

		self.source = source
		self.variables = []
		with open(source, 'r') as file:
			self.lines = file.readlines()

		# Declaritive Start
		self.create_line_objects()
		self.assign_object_values()
		# Declaritive End

	def __repr__(self): return f'{self.lines}'

	def get_indent_level(string):

		# Supports inconsistant use of
		# tabs and spaces, but will reformat
		# all leading whitespace to tabs

		count = 0

		for charachter in string:
			if charachter == ' ': count += 1
			elif charachter == '\t': count += 1
			else: return count

		return count

	def create_line_objects(self):

		openers = ['{', '[', '"']
		numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

		case_opener = 0
		case_closer = 1
		case = {
		'list': ['[', ']'],
		'str': ['"', '"'],
		'int': ['int(', ')'],
		'float': ['float(', ')']
		}

		line_number = 0
		new_file_lines = []
		old_parent = 'none'
		current_parent = 'none'
		current_type = None
		parent_stack = []
		parent_name = 'none'

		for line in self.lines:

			line = line.strip('\n')
			exec(f'self.line{line_number} = private.line()')
			indent_level = pyon.get_indent_level(line)
			empty_line = line.split() == []
			is_assignment = False

			if not empty_line: is_assignment = line[-1] == ':'

			if is_assignment:
				line_array = line.strip(':').split()
				assigner = line_array[-1]
				type = line_array[-2]
				content = line_array
				old_parent = current_parent
				parent_name = current_parent
				current_parent = assigner
				current_type = type
				exec(f'self.{assigner} = private.block(self)')
				exec(f'self.{assigner}.block_start = line_number')
				exec(f'self.{assigner}.type = {type}')
				exec(f'self.{assigner}.content = {type}()')
				exec(f'self.{assigner}.child_indent = {indent_level + 1}')
				exec(f'self.variables.append("{assigner}")')

				nested = indent_level != 0
				new_base_block = not nested
				child_indent_level = indent_level + 1

				if new_base_block:
					parent_stack = [(child_indent_level, current_parent)]
				else:
					parent_stack.append((child_indent_level, assigner))
					for p in parent_stack:
						if p[0] == indent_level:
							parent_name = p[1]
							exec(f'pyon.storage = self.{p[1]}')
							old_parent = pyon.storage
			else:
				not_number = content[-1][0] not in numbers
				not_typed = content[-1][0] not in openers
				content = [line.strip('\t').strip(' ')]
				if not_number and not_typed: content[-1] = f'{content[-1]}'

			exec(f'self.line{line_number}.parent_name = current_parent')
			exec(f'self.line{line_number}.is_assignment = {is_assignment}')
			exec(f'self.line{line_number}.parent = self.{current_parent}')
			exec(f'self.line{line_number}.line_number = {line_number}')
			exec(f'self.line{line_number}.indent_level = {indent_level}')
			exec(f'self.line{line_number}.content = {content}[-1]')
			exec(f'self.line{line_number}.type = "{current_type}"')
			exec(f'new_file_lines.append(self.line{line_number})')

			if is_assignment and indent_level == 0:
				exec(f'self.line{line_number}.parent_name = "none"')
				exec(f'self.line{line_number}.parent = "none"')
				exec(f'self.{assigner}.parent = "none"')
			elif is_assignment and indent_level != 0:
				exec(f'self.line{line_number}.parent_name = parent_name')
				exec(f'self.line{line_number}.parent = old_parent')
				exec(f'self.{assigner}.parent = old_parent')

			line_number += 1

		self.lines = new_file_lines

	def assign_object_values(self):

		case_opener = 0
		case_closer = 1

		case = {
		'list': ['[', ']'],
		'str': ['"', '"'],
		'int': ['int(', ')'],
		'float': ['float(', ')']
		}

		reversed_file = self.lines[::-1]
		variables = self.variables
		current_assigner = ''
		ignore = ['int', 'float', 'none']


		# the file is reversed sothat the
		# nests are handled deepest first
		for line in reversed_file:

			opener = case[line.type][case_opener]
			closer = case[line.type][case_closer]

			if line.parent != 'none' and len(line.content) != 0:

				if line.is_assignment:

					line.parent.variables.insert(0, line.content)
					exec(f'line.parent.content += line.parent.type(self.{line.content}.content)')
				else:
					line.parent.lines.insert(0, line)
					if line.content not in variables:
						exec(f'line.parent.content += {opener}{line.content}{closer}')

		for line in self.lines:

			not_assignment = line.is_assignment == False
			is_variable = line.content in variables

			# contents of lists are reversed
			# because they were added backwards
			# because the file was reversed as seen aboce
			if line.is_assignment and line.type == 'list':

				exec(f'self.{line.content}.content = self.{line.content}.content[::-1]')

			if is_variable and not_assignment:

				exec(f'line.parent.content += self.{line.content}.content')

	def read(self): return self.variables

	def read_all(self): return self.lines

	def append(self, string):

		if string == '':
			with open(self.source, 'a') as source: source.write('\n')
			return 0

		case_opener = 0
		case_closer = 1

		case = {
		'list': ['[', ']'],
		'str': ['str(', ')'],
		'int': ['int(', ')'],
		'float': ['float(', ')']
		}


		string = str(string)
		is_assignment = string[-1] == ':'
		if string[0] != '[' and string[0] != '{': number_of_words = len(string.split())
		else:
			if is_assignment == False: number_of_words = 1
		line_number = self.lines[-1].line_number + 1

		if is_assignment: for_type_check = string.split()[0]
		else: for_type_check = string
		exec(f'pyon.storage = type({for_type_check})')
		line_type = f'{pyon.storage}'.split()[-1].strip('>').strip("'")

		problem = False
		if number_of_words == 0 or number_of_words > 2: problem = True
		if is_assignment and number_of_words != 2: problem = True
		if is_assignment and line_type != 'type': problem = True
		if is_assignment == False and number_of_words != 1: problem = True
		if problem: raise SyntaxError('Improperly formated string')

		# wow, mind blown. i dont need all those execs XD
		exec(f'self.line{line_number} = private.line()')
		exec(f'pyon.storage = self.line{line_number}')
		new_line = pyon.storage

		if is_assignment:

			line_type = string.split()[0]
			content = string.strip(':').split()[-1]
			parent = 'none'
			parent_name = 'none'
			indent_level = 0

			exec(f'self.{content} = private.block(self)')
			exec(f'self.{content}.block_start = line_number')
			exec(f'self.{content}.type = line_type')
			exec(f'self.{content}.child_indent = {indent_level + 1}')
			exec(f'self.{content}.content = {line_type}()')
			self.variables.append(content)

		else:

			last_line = self.lines[-1]
			if last_line.is_assignment: exec(f'pyon.storage = self.{last_line.content}')
			else: pyon.storage = last_line.parent
			parent = pyon.storage

			content = string
			parent_name = self.lines[-1].parent_name
			indent_level = parent.child_indent

		new_line.parent_name = parent_name
		new_line.line_number = line_number
		new_line.indent_level = indent_level
		new_line.is_assignment = is_assignment
		new_line.type = line_type
		new_line.parent = parent
		new_line.content = content

		leading_whitespace = '\t' * new_line.indent_level
		self.lines.append(new_line)

		if is_assignment == False:

			opener = case[new_line.parent.type][case_opener]
			closer = case[new_line.parent.type][case_closer]

			exec(f'parent.content += {opener}{content}{closer}')
			parent.lines.append(new_line)

		with open(self.source, 'a') as source: source.write(f'{leading_whitespace}{string}\n')

	def write(self, string):

		problem = False
		if string != '' and len(string.split()) != 2: problem = True
		if string != '' and string[-1] != ':': problem = True
		if problem: raise SyntaxError('Write requires argument to declare a variable')

		with open(self.source, 'w') as file: file.write(string)
