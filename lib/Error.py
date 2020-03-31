########################################################
## Module  : Error         ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from .Main import *


########################################################
## ------- here starts the module definitions ------- ##
########################################################
types = {
    'alert'      : '\033[93m',
    'error'      : '\033[91m',
    'information': '\033[94m',
    'end'        : '\033[0m',
    'bold'       : '\033[1m',
    'line'       : '\033[4m'
}

def write(string, type, end='end'):
    return types[type.lower()] + str(string) + types[end.lower()]

class new(dict):
    type = 'error'

    def print(self, end='end'):
        header = '%s in %s' % (self.type, self.name) if self.name else self.type
        string = write(header.capitalize(), self.type) + ' { '
        if self.error:
            string += str(self.error) + ', '
        for k, v in self.items():
            string += '%s: %s, ' % (write(str(k).capitalize(), 'bold'), repr(v))
        print(string[0 : -2] + ' }')

    def __repr__(self):
        devolve = ('%s in %s' % (self.type, self.name) if self.name else self.type).capitalize() + ' { '
        if self.error:
            devolve += str(self.error) + ', '
        for k, v in self.items():
            devolve += '%s: %s, ' % (str(k).capitalize(), repr(v))
        return devolve[0 : -2] + ' }'

    def __str__(self):
        return self.__repr__()

    def __init__(self, name=None, error=None, **argsk):
        self.error = error
        self.name = name
        self.update(argsk)
        self.print()

class alert(new):
    type = 'alert'

class infor(new):
    type = 'information'

def check(self):
    return isinstance(self, new)

def delete(self):
    Object.delete(self, '__error__')

def get(self):
    error = Object.get(self, '__error__')
    return error if isinstance(error, new) else None

def set(self, error):
    Object.set(self, '__error__', error)

def stop(self, **argsk):
    if check(self):
        Error = print(self, isdevolve=True, **argsk)
        raise Exception(Error)

# end module
setModule(__name__, '__call__', new)
