########################################################
## Module  : PyDoc         ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from . import Array, Json, String
from .Main import *

# fixed variables
_open = open

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def addtag(devolve, strip, path):
    isexec, istags, istext  = False, False, False
    if strip[-1] == ':': istags, strip = True, strip[ : -1].strip()
    elif strip[-3 : ] in ['\'\'\'', '"""']: istext, strip = strip[-3 : ], strip[ : -3].strip()
    if strip[-1] in '}]':
        for head in ['{}', '[]']:
            if strip[-1] == head[1]:
                isattr = strip.find(head[0])
                tag = strip[ : isattr].strip().lower()
                if isattr > len(tag):
                    attr = strip[isattr + 1 : -1]
                    if head[0] == '[': isexec, istags = True, False
                else:
                    Array.clear(devolve)
                break
    else:
        attr, tag = '', strip.lower()
    current = Array.path(devolve, path)
    item = Array.new()
    item['name'] = tag
    item['index'] = len(current)
    if isexec:
        item['attr'] = Array.new()
        item['head'] = attr
        item['exec'] = ''
    else:
        item['attr'] = Json.decode('{%s}' % attr) if attr else Array.new()
        if istext: item['text'] = ''
        elif istags: item['tags'] = Array.new()
    if isexec or istext or istags:
        path.append(item['index'])
        if istags: path.append('tags')
        current += item
        if isexec: return 2
        elif istext: return istext
        else: return 1
    else:
        current += item
    return 0

def decode(string):
    addspace, devolve, path, spaces = 0, Array.new(), [], []
    for line in string.splitlines():
        strip = line.strip()
        if not strip[ : 1] in ['', '#']:
            countrim = String.countrim(line)[0]
            if len(path) > 0:
                add = True
                if isinstance(addspace, str):
                    if strip == addspace and (countrim == spaces[-1] if len(spaces) > 0 else countrim == 0):
                        add = False
                        addspace = 0
                        del path[-1]
                elif addspace in [1, 2]:
                    if countrim > spaces[-1] if len(spaces) > 0 else countrim > 0:
                        spaces.append(countrim)
                    else:
                        Array.clear(devolve)
                        break
                    addspace = 0 if addspace == 1 else 3
                elif spaces[-1] > countrim:
                    del spaces[-1]
                    if isinstance(path[-1], int): del path[-1]
                    else: path = path[ : -2]
                    addspace = 0
                if add:
                    if len(path) > 0:
                        if isinstance(path[-1], int):
                            parent = Array.path(devolve, path)
                            if addspace == 3:
                                parent['exec'] += '%s\n' % line[spaces[-1] : ].rstrip()
                            else:
                                parent['text'] += '%s\n' % line
                        else:
                            addspace = addtag(devolve, strip, path)
                    else:
                        addspace = addtag(devolve, strip, path)
            else:
                addspace = addtag(devolve, strip, path)
    return devolve

def encode(array, spaces=0):
    string = ''
    for index, tag in Array.items(array):
        try:
            if isinstance(tag['name'], str) and Array.iskeys(tag['attr']):
                space = ' ' * (spaces * 4)
                string += space +tag['name']
                if tag['attr'] and not Array.iskey(tag, 'exec'): string += ' ' + Json.encode(tag['attr'], False, True)

                if Array.iskey(tag, 'exec'):
                    string += ' [%s]:\n' % tag['head']
                    for line in tag['exec'].splitlines():
                        string += '%s%s%s\n' % (space, ' ' * 4, line)
                elif Array.iskey(tag, 'text'):
                    string += ' """\n'
                    string += tag['text']
                    string += space + '"""\n'
                elif Array.iskey(tag, 'tags'):
                    string += ':\n'
                    string += encode(tag['tags'], spaces + 1)
                else:
                    string += '\n'
        except:
            string = ''
            break
    return string

def open(path):
    return decode(_open(path, 'r').read())

def save(array, path):
    file = _open(path, 'w')
    file.write(encode(array))
    file.close()
