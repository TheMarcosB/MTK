########################################################
## Module  : Open          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import os

# import default modules
from .Main import Paths as _Paths, setModule
from . import Auto, Paths

# fixed variables
_open = open

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# file
def open(path, mode='r'):
    return _open(path, mode)

def read(path):
    try: return open(path).read()
    except: return ''

def auto(path, *argsv, **argsk):
    try: return Auto.get(path)(red(path), *argsv, **argsk)
    except: pass

def write(path, content, mode='w', encode=None):
    try:
        encode = Auto.set(path)
        file = open(path, mode)
        file.write(encode(content) if encode else content)
        file.close()
    except:
        pass

class new(Paths.new):
    __callbacks__ = {'auto': auto, 'read': read, 'open': open, 'write': write}

# end
setModule(__name__, '__call__', new)
