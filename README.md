# What is PYON

PYON stands for Python Object Notation.  
It's meant to be a more python friendly  
way to store and read data with python.  
PYON files are meant to be maintainable  
and readable by both humans and computers.

# Using PYON

initialising a pyon file is done like so:
<pre>
>>> from pyon import pyon  
>>> doc = pyon('document.pyon')
</pre>
it can now be read from and written to.  
think of it as being similar to
<pre>
>>> open('file.txt', 'rw')
</pre>


pyon files should be formatted by declaring  
a type followed by a variable name followed  
by ':' then on a new line, indented, then  
start adding data to the variable.

like so:
<pre>
type my_first_variable:  
	data  
	data  
	data  
	type nested_variable:  
		data

type my_second_variable:  
	my_first_variable
</pre>
think of it as being similar to declaring  
a class.
<pre>
>>> class my_first_class:  
>>>	self.data = data
</pre>
the type must be a python built in type.  
data is added to variables by enclosing  
it in the appropriate openers and closers  
then converting the data to the variables  
type, then using python's '+' operator.

e.g.
<pre>
list variable:  
	1    
	2.0
	'three'  
	[4, 'five']
</pre>
would be handled like so:  
<pre>
>>> variable = list()  
>>> variable += list([1])  
>>> variable += list([2.0])  
>>> variable += list(['three'])  
>>> variable += list([[4, 'five']])
</pre>
which would be equivelent to:
<pre>
>>> variable = [1, 2.0, 'three', [4, 'five']]
</pre>
this means, for example, that an int can  
be placed under a list variable, but a list  
cannot be placed under an int variable  
because a list can be created that holds an int,  
but an int cannot be created that holds a list.

after a pyon file has been opened,  
data can be retrieved using  
{filename}.{variable}.content.  

e.g.
<pre>
>>> from pyon import pyon  
>>> doc = pyon('document.pyon')  
>>> print(doc.my_variable.content)  
</pre>
for every line in the file, line object is  
created. this object is named line{line_number}.  
it contains the line's number, indentation level,  
{parent variable object}, {parent variable name},  
type, content, and wheather or not the line is a  
declaration or not.

this means the line object can be retrieved like so:
<pre>
>>> print(line5)
</pre>
and the line's content can be retrieved like so:
<pre>
>>> print(line5.content)
</pre>
note though, that .content returns the line's content  
without any leading whitespace or ending ':'

to properly reconstruct the line, use:
<pre>
>>> print(line5.reconstruct())
</pre>


READ METHODS are as follows:
-
<pre>
>>> doc = pyon('document.pyon')  
>>> doc.read()
</pre>
returns a list of all variables declared in  
the file
<pre>
>>> doc.read_all()
</pre>
returns a list of array representations of  
all line objects in the file
<pre>
>>> doc.{variable}.read()
</pre>
returns the the variables declared  
immediatly within {variable}  
(does not return variables declared  
within those variables)
<pre>
>>> doc.{variable}.read_all()
</pre>
returns a list of array representations of  
all line objects declared immediatly  
within {variable}

WRITE METHODS are as follows:
-
<pre>
>>> doc = pyon('document.pyon')  
>>> doc.append('list I_use:')  
>>> doc.I_use.append('"Arch"')  
>>> doc.I_use.append('"btw"')
</pre>
NOTE that strings are appended surrounded by  
qoutes within the string. if this is not done  
pyon will see it as either a number or a variable.

{file}.append() takes 1 string as an argument.  
it formats this string and adds it as the  
last line of the pyon file.

if a variable is declared, it will chrate  
a new block and the variable will have no  
parents or indentation. otherwise, if a  
variable is not declared, it will nest the  
new value in the first layer of the last  
block in the file.

{file}.{variable}.append() does the same as  
{file}.append() but to the last line of  
the variable always. it never looks for  
a parent variable.

for both append methods, if an empty string  
is parsed, it will append a new line.

{file}.write() overwrites the entire file  
with a new, specified, variable declaration.  
if the argument parsed into write() is not  
a variable declaration, a syntax error  
will be raised.

{file}.{variable}.write() overwrites an entire  
variable, including its declaration. thas,  
{file}.{variable}.write('') can be used to  
delete a variable from the file.

for a demonstration of pyon, see main.py  
and doc.pyon
