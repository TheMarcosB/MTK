########################################################
## Module  : Database      ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from .Main import *
from . import Array, Blocker, Class, Error

# fixed variables
_open = open
chaCoding = [('&{1}', '#'), ('&{2}', '$'), ('&{3}', ':'), ('&{4}', ';'), ('&{5}', ']'), ('&{6}', '['), ('&{7}', ',')]

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# get
def getvalue(string):
	for encode, decode in chaCoding:
		string = string.replace(encode, decode)
	return string
	
def get(string):
	header, values = {}, []
	for line in string.splitlines():
		line = line.lstrip()
		if line != '' and line[0] != '#':
			if line[0] == '$':
				split = line.split(':')
				key = split[0][1 : ].strip()
				val = split[1].strip()
				if val != '' and val[0] == '[' and val[-1] == ']':
					value = []
					for item in val[1 : -1].split(','):
						value.append(getvalue(item.strip()))
				else:
					value = getvalue(val)
				header[key] = value
			else:
				if header.get('types') and isinstance(header['types'], (list, tuple)):
					index, items = 0, []
					for item in line.split(';'):
						try:
							item, _type= getvalue(item), header['types'][index]
							if _type == 'bool':
								if item == '0': item = False
								else: item = True
							elif _type == 'list':
								item = item.split(',')
							elif _type == 'number':
								try: item = int(item)
								except: item = float(item)
							items.append(item)
							index += 1
						except:
							items.append(getvalue(item))
					values.append(items)
				else:
					values.append(line.split(';'))
	return header, values
			
# set
def setvalue(string):
	for encode, decode in chaCoding:
		string = string.replace(decode, encode)
	return string


# search
def _values(self, values):
	devolve, keys, index = Array.new(), Object.get(self, '__head__')['keys'], 0
	for value in values:
		devolve[keys[index]] = value
		index += 1
	return devolve
	
def _labels(self, query, values):
	devolve, keys = False, Object.get(self, '__head__')['keys']
	for k, v in Array.items(query):
		try:
			index = keys.index(k)
			if Array.isarray(values[index]):
				if len(values[index]) > 0:
					if Array.isarray(v):
					    for tag in Array.values(v):
						    devolve = False
						    for val in values[index]:
							    if str(tag).lower() == str(val).lower():
								    devolve = True
								    break
						    if not devolve: break
					else:
						for val in values[index]:
							if str(v).lower() == str(val).lower():
								devolve = True
								break
			elif str(v).lower() == str(values[index]).lower():
				devolve = True
		except:
			break
	return devolve
        
def search(self, query):
	devolve = []
	for values in self.__list__:
		try:
			if isinstance(query, str) and query.lower() in Array.tostring(values).lower():
				devolve.append(_values(self, values))
			elif isinstance(query, (tuple, list)) and query[0].lower() in Array.tostring(values).lower():
				if _labels(self, query[1], values):
					devolve.append(_values(self, values))
			elif isinstance(query, (dict, Array.new)):
				if _labels(self, query, values):
					devolve.append(_values(self, values))
		except:
			pass
		
	return devolve

# data
class database(Class.new):
	def login(self, *argsv, **argsk):
		Blocker.enter(self, *argsv, **argsk)
		
	def __mod__(self, query):
		return Array.new(search(self, query))
		
	def __init__(self, string):
		header, values = get(string)
		self.__list__ += values
		Object.get(self, '__head__').update(header)
		if header.get('username') and header.get('password'):
			Blocker.new(self, header['username'], header['password'])
		elif header.get('username'):
			Blocker.new(self, None, header['username'])
		elif header.get('password'):
			Blocker.new(self, None, header['password'])
			
def open(path):
	return database(_open(path, 'r').read())
