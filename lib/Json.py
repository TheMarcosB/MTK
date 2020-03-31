########################################################
## Module  : Json          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from . import Array, Class, Error
from .Main import *

# fixed variables
_not_val = ['{', '[', ':', ',', '\'', '"', ']', '}']
_not_key = _not_val + [' ']
_open = open
_swap_decode = '\\',   '\n',  '\r',  '\t',  '"',   '\''
_swap_encode = '\\\\', '\\n', '\\r', '\\t', '\\"', '\\\''

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# decode
def _realdecode(string):
    string = swapStr(string, _swap_encode, _swap_decode)
    string = string.replace('\\', '')
    string = string.replace('${/}', '\\')
    return realStr(string)

def _current(string):
    return string.replace('\\\\', '${/}')

def decode(string, file=None):
    devolve = Array.new()
    count, error, status = 0, None, 0 # check
    path, pathcount, prev = [], 0, None # path
    ispoint = isstart = False # number
    key = value = None # string
    opened, closed, openst = [], string.rfind('}'), None # split
    for i in string:
        # main
        if i == '{' and len(opened) == 0: # open
            opened.append(i)
        elif i == '}' and count == closed and key == value == None: # close
            try:
                del opened[0]
            except:
                error = Error('json', error='No close', file=file)
                break
        # array open
        elif (i in ['{', '['] and status == 5) or (i == '[' and pathcount == 0 and status == 0):
            if opened[-1] == '[' or status == 0:
                _array = Array.path(devolve, path)
                _index = len(_array)
                _array += Array.new()
                path.append(_index)
            else:
                path.append(_realdecode(key))
                Array.path(devolve, path, new=Array.new())
            key = None
            value = None
            opened.append(i)
            pathcount += 1
            if i == '[': status = 5
            else: status = 0
        # key
        elif i in ['"', '\''] and status == 0 and opened[-1] == '{' and not isstart: # string open
            key = ''
            openst = i
            status = 1
        elif i == openst and status == 1 and key[-1 : ] != '\\': # string close
            status = 2
        elif i.isalnum() and status == 0 and opened[-1] == '{' and not isstart: # alpha
            key = i
            status = 3
        elif i.isdigit() and status == 0 and opened[-1] == '{': # number
            key = ''
            if isstart:
                key += isstart
                isstart = False
            key += i
            status = 4
        # split
        elif i == ':' and status in [2, 3, 4]:
            ispoint = False
            status = 5
        # less and more
        elif i == '-' and status in [0, 5]:
            isstart = i
        # value
        elif i in ['"', '\''] and status == 5 and not isstart: # string open
            value = ''
            openst = i
            status = 6
        elif i == openst and status == 6 and value[-1 : ] != '\\': # string close
            status = 7
        elif not i in _not_key and status == 5 and not isstart: # alpha
            value = i
            status = 8
        # key append
        elif key != None and status == 1: # string
            key = _current(key + i)
        elif key != None and i.isalnum() and status == 3: # alpha
            key += i
        elif key != None and (i.isdigit() or (i == '.' and not ispoint)) and status == 4: # number
            key += i
            if i == '.': ispoint = True
        # value append
        elif value != None and status == 6: # string
            value = _current(value + i)
        elif value != None and not i in _not_val and status == 8: # alpha
            value += i
        # item close
        elif status in [0, 5, 7, 8] and i in [',', ']', '}']:
            if status > 0:
                if opened[-1] == '[' and value != None:
                    Array.path(devolve, path, add=_realdecode(value))
                    status =  5
                elif not opened[-1] == '[' and key != None and value != None:
                    Array.path(devolve, path + [_realdecode(key)], new=_realdecode(value))
                    status = 0
                elif (i, prev) == (',', ','):
                    error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i)
                    break
                elif i == ',':
                    status = 5 if opened[-1] == '[' else 0
            elif (((i == '}' and len(path) == 0) or i == ',') and key == '') or ((i, prev) == (',', ',')):
                error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i, file=file)
                break
            elif i == ',':
                status = 5 if opened[-1] == '[' else 0
            if i in [']', '}']:
                try:
                    if count != closed: del path[-1]
                    del opened[-1]
                except:
                    error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i, file=file)
                    break
            prev = i
            key = None
            value = None
            ispoint = False
        # array close
        elif i in [']', '}'] and len(path) > 0:
            try:
                del path[-1]
                del opened[-1]
                status = 5 if opened[-1] == '[' else 0
            except:
                error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i, file=file)
                break
        elif not i in ['\n', ' ']:
            error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i, file=file)
            break
        count += 1
    if not error and not (len(path) == len(opened) == 0):
        error = Error('json', error='no close', file=file)
    if error: Array.clear(devolve)
    return devolve

def open(path):
    return decode(_open(path, 'r').read(), path)

def sys(name):
    return open('%s/json/%s.json' % (Paths.etc, name))

# encode
def _isalpha(string):
    for i in _not_str:
        if i in string: return False
    return True

def _realencode(value, isalpha):
    if value == None: return 'null'
    elif isinstance(value, (bool, float, int)): return str(value).lower()
    elif isinstance(value, str) and isalpha and _isalpha(value): return value
    else: return '"%s"' % (swapStr(str(value), _swap_decode, _swap_encode))

def _encode(array, isspace, isalpha, space=''):
    try:
        iscount = Array.iscount(array)
        devolve = '[' if iscount else '{'
        count = 1
        items = Array.items(array)
        length = len(items)
        if not iscount and isspace and length > 1: devolve += '\n'
        for k, v in items:
            if not iscount and isspace and length > 1: devolve += space + (' ' * 4)
            if not iscount: devolve += _realencode(k, isalpha) + ': '
            count += 1
            if Array.isarray(v): devolve += _encode(v, isspace, isalpha, space + (' ' * 4))
            else: devolve += _realencode(v, isalpha)
            if length >= count:
                if not iscount and isspace: devolve += ',\n'
                else: devolve += ', '
        if not iscount and isspace and length > 1: devolve += '\n' + space
        return devolve + (']' if iscount else '}')
    except:
        return '{}'

def encode(array, isspace=True, isalpha=False):
    return _encode(array, isspace, isalpha)
