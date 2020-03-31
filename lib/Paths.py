########################################################
## Module  : Paths         ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################
# import default module
import os

# import local modules
from .Main import *

# fixed variables
callbacks = {
    'exists': os.path.exists,
    'isdir': os.path.isdir,
    'isfile': os.path.isfile,
    'ls': os.listdir,
    'listdir': os.listdir
}

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# path class
class new(str):
    __callbacks__ = {}
    __callback__ = None

    def __getattr__(self, key):
        new = self.__class__
        if key in callbacks.keys(): return new('%s/%s' % (self, key), (callbacks[key], self))
        elif key in self.__callbacks__.keys(): return new('%s/%s' % (self, key), (self.__callbacks__[key], self))
        else: return new('%s/%s' % (self, key))

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __call__(self, *argsv, **argsk):
        callback = self.__callback__
        if callback:
            try: return callback[0](str(callback[1]), *argsv, **argsk)
            except: pass

    def __init__(self, string=None, call=None):
        if call: self.__callback__ = call

    def __new__(cls, string=None, *argsv, **argsk):
        if not string or string[ : 1] != '/': string = os.getcwd()
        return str.__new__(cls, string)

# system path
def system(self, key):
    try: return new(getattr(Paths, key))
    except: return new(getattr(Paths, 'local'))

def current(self):
    return new()

# end
setModule(__name__, '__call__', current)
setModule(__name__, '__getattr__', system)
setModule(__name__, '__getitem__', system)
