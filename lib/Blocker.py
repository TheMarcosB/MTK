########################################################
## Module  : Blocker       ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# fixed variables
booleans = {}

# import local modules
from . import Error
from .Main import *

########################################################
## ------- here starts the module definitions ------- ##
########################################################
class boolean:
    def allow(self, username=None, password=None, *argsv):
        return self.username == username and self.password == password

    def enter(self, username=None, password=None, *argsv, **argsk):
        if self.allow(username, password):
            self.boolean = True

    def exit(self, username=None, password=None, *argsv, **argsk):
        if self.allow(username, password):
            self.boolean = False

    def set(self, enter=None, new=None, *argsv):
        try:
            allow = self.allow(*enter)
        except:
            allow = False
            Error('blocker', "change requires ('username' and 'password') current in '%s'" % clsName(self.cls))
        if allow:
            try:
                self.username, self.password, *args = new
            except:
                Error('blocker', "change requires new ('username' and 'password') in '%s'" % clsName(self.cls))

    def setUsername(self, enter=None, new=None, *argsv, **argsk):
        self.set(enter, (new, self.password))

    def setPassword(self, enter=None, new=None, *argsv, **argsk):
        self.set(enter, (self.username, new))

    def __bool__(self):
        return self.boolean

    def __eq__(self, compare):
        return self.boolean == compare

    def __init__(self, cls, username=None, password=None, *argsv, **argsk):
        self.cls = cls
        self.boolean = False
        self.password = password
        self.username = username

def _get(self):
    return booleans[self.__id__]

class current:
    def check(self):
        try: return bool(_get(self))
        except: return True

    def new(self, *argsv):
        booleans[self.__id__] = boolean(self, *argsv)

    def enter(self, *argsv):
        try: _get(self).enter(*argsv)
        except: pass

    def exit(self, *argsv):
        try: _get(self).exit(*argsv)
        except: pass

    def set(self, *argsv):
        try: _get(self).set(*argsv)
        except: pass

    def setUsername(self, *argsv):
        try: _get(self).setUsername(*argsv)
        except: pass

    def setPassword(self, *argsv):
        try: _get(self).setPassword(*argsv)
        except: pass

def new(self, *argsv):
    try: self.__blocker__.new(self, *argsv)
    except: pass

def check(self):
    try: return self.__blocker__.check(self)
    except: return False

def enter(self, *argsv):
    try: self.__blocker__.enter(self, *argsv)
    except: pass

def exit(self, *argsv):
    try: self.__blocker__.exit(self, *argsv)
    except: pass

def set(self, *argsv):
    try: self.__blocker__.set(self, *argsv)
    except: pass

def setUsername(self, *argsv):
    try: self.__blocker__.setUsername(self, *argsv)
    except: pass

def setPassword(self, *argsv):
    try: self.__blocker__.setPassword(self, *argsv)
    except: pass

def status(self):
    return 'opened' if check(self) else 'closed'
