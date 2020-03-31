########################################################
## Module  : Settings      ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from . import Array, String, Sys
from .Main import *

# fixed variables
_open = open

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def realval(string, ls=True):
    if ls and string[ : 1] == '[' and string[-1 : ] == ']':
        items = Array.new()
        for item in string[1 : -1].split(','):
            items += realval(item.strip(), False)
        return items
    elif ls and string[ : 1] == '(' and string[-1 : ] == ')':
        items = tuple()
        for item in string[1 : -1].split(','):
            items += (realval(item.strip(), False), )
        return items
    elif (string[ : 1] == '"' and string[-1 : ] == '"') or (string[ : 1] == "'" and string[-1 : ] == "'"):
        return string[1 : -1]
    else:
        return realStr(string)

# data
def decode(string):
    data = Array.new()
    if isinstance(string, str):
        count = 0
        name = None
        for line in string.splitlines():
            line = line.strip()
            if line != '' and line[0] != '#':
                if line[0] == '[' and line[-1] == ']':
                    name = realStr(line[1 : -1].strip())
                    data[name] = {}
                    count = 0
                else:
                    div = line.find('=')
                    if div != -1:
                        key = realStr(line[ : div].strip())
                        val = line[div + 1 : ].strip()
                    else:
                        key = count
                        val = line
                        count += 1
                    if name != None: data[name][key] = realval(val)
                    else: data[key] = realval(val)
    return data

def encode(data, start=True):
    string = ''
    for k, v in data:
        if isinstance(v, tuple):
            if isinstance(k, str): string += k + ' = '
            string += '(%s)\n' % String.format('%s, ', v, False)
        elif Array.iscount(v):
            if isinstance(k, str): string += k + ' = '
            string += '[%s]\n' % String.format('%s, ', v, False)
        elif not isinstance(v, (Array.new, dict)):
            if isinstance(k, str): string += k + ' = '
            string += '%s\n'% str(v)
    if start:
        for k, v in data:
            if isinstance(v, (Array.new, dict)):
                string += '[%s]\n%s' % (k, encode(v, False))
    return string

# file
def open(path):
    data = decode(_open(path, 'r').read())
    Object.set(data, '__save__', path)
    return data

def save(data):
    if isinstance(data, Array.new):
        path = Object.get(data, '__save__')
        file = _open(path, 'w')
        file.write(encode(data))
        file.close()

def sys(name):
    return open('%s/conf/%s.conf' % (Paths.etc, name))
