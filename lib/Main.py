########################################################
## Module  : Main          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import os, re, sys, time

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def Types(items, type):
    for item in items:
        if not isinstance(item, type):
            return False
    return True

# paths
class Paths:
    lib = os.path.dirname(os.path.realpath(__file__))
    local = os.path.dirname(lib)
    etc = local + '/etc'
    home = os.getenv('HOME')
    img = local + '/img'
    data = home + '/.TheMarcosData'

def Date(data = '%d/%m/%Y' + ' at ' + '%H:%M:%S'):
    return time.strftime(data)

# string
class lockStr(str):
    def __iadd__(self, value):
        return self

    def __imul__(self, value):
        return self

    def __new__(cls, string):
        return str.__new__(cls, string)

def realStr(string):
    if string.lower() == 'false': return False
    elif string.lower() == 'true': return True
    elif string.lower() in ['none', 'null', 'undefined']: return None
    elif re.search('^-?\d+\.\d+$', string): return float(string)
    elif re.search('^-?\d+$', string): return int(string)
    else: return string

def swapStr(string, old, new=None, clean=''):
    for i in (range(len(old)) if new != None else old):
        try: string = string.replace(*((old[i], new[i]) if new != None else (i[0], i[1])))
        except: string = string.replace(old[i] if new != None else i[0], clean)
    return string

# class
class Object:
    def delete(self, key):
        try: object.__delattr__(self, key)
        except: return False
        return True

    def exists(self, key):
        try: object.__getattribute__(self, key)
        except: return False
        return True

    def attr(self, key):
        try: return object.__getattribute__(self, key)
        except: pass

    def dict(self):
        return Object.attr(self, '__dict__')

    def dir(self):
        return  object.__dir__(self)

    def attrs(self):
        return list(set(Object.dir(self) + ['__self__'] + list(Object.dict(self).keys())))

    def get(self, key):
        return Object.dict(self).get(key)

    def set(self, key, value):
        try: Object.dict(self)[key] = value
        except: return False
        return True

def setModule(name, key, value):
    class new_module(sys.modules[name].__class__):
        locals().update({key: value})
    sys.modules[name].__class__ = new_module

def clsName(self):
    try:
        name = self.__name__
        if isinstance(name, str): return name
        else: return object.__getattribute__(self, '__class__').__name__
    except:
        return object.__getattribute__(self, '__class__').__name__

# items
def getItem(self, key, default=None):
    try:
        if isinstance(key, (list, tuple)):
            for k in key: self = self[k]
            return self
        else:
            return self[key]
    except:
        return default

def setItem(self, key, value):
    try:
        if isinstance(self, tuple):
            self = list(self)
            if isinstance(key, (list, tuple)):
                if not isinstance(key, list): key = list(key)
                key, keys = key[0], key[1 : ]
                if len(keys) > 0: value = setItem(self[key], keys, value)
            self[key] = value
            return tuple(self)
        elif isinstance(key, (list, tuple)):
            count = 1
            for k in key:
                if count == len(key): self[k] = value
                else: self = self[k]
                count += 1
        else:
            self[key] = value
    except:
        pass
    return self

def getKeys(self, keys, default=None):
    devolve = {}
    for key in keys: devolve[key] = self.get(key, default)
    return devolve

def getArg(argsk, key, argsv, index):
    return argsk.get(key, getItem(argsv, index))

#  number
def isNum(value):
    return isinstance(value, (float, int))

def getNum(number, _min, _max):
    try: return min(max(number, _min), _max)
    except: return _min

def getOne(number):
    return getNum(number, 0, 1)

def get100(number):
    return getNum(number, 0, 100)

# cache file
class Cache:
    # read
    def read(self, isempty=True):
        try: return open(self.path, 'r').read()
        except: return self.empty if isempty else ''

    def lines(self):
        return self.read().splitlines()

    # write
    def write(self, string, isupdate=False):
        old = self.read(isempty=False)
        file = open(self.path, 'w')
        file.write(old + string if isupdate else string)
        file.close()

    def append(self, string):
        self.write(string, isupdate=True)

    def delline(self, *argsv):
        string = ''
        for line in self.lines():
            if not line in list(argsv):
                string += '%s\n' % (line)
        self.write(string)

    def newline(self, *argsv):
        string = ''
        for line in argsv: string += '%s\n' % (line)
        self.write(string, isupdate=True)

    # main
    def __init__(self, path, empty=''):
        self.empty = empty
        self.path = os.path.realpath(path)
