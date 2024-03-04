from pyon import pyon

def main():
	print('Running...\n')
	doc = pyon('doc.pyon')
	doc.write('None pwnd:')
	# reconstruction tests
	"""
	reconstructed_file = ''
	for line in doc.lines: reconstructed_file += line.reconstruct() + '\n'

	print(reconstructed_file)
	"""

	# read tests
	"""
	print()
	print(doc.numbers.read_all()[0].content)
	print()
	print(doc.numbers.content)
	print()
	print(doc.super.content)
	print()
	print(doc.intagers.content)
	print()
	print(doc.numbers + 1)
	print()
	print(doc.second.content)
	print(doc.line3.content)
	"""

	# write tests
	"""
	doc.append('')
	doc.append('list append_test:')
	doc.append('"1"')
	doc.append('2')
	print(doc.append_test.content)
	doc.append('list fart:')
	doc.append('"five"')
	doc.append('"six"')
	doc.append('[7, 8]')
	doc.numbers.append('"hi"')
	doc.numbers.append('')
	"""

if __name__ == '__main__': main()
