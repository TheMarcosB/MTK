########################################################
## Module  : MTK.Get       ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from ..Main import *

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def getData(self):
    return Object.get(self, '__data__')

def getKey(self):
    return Object.get(self, '__key__')

def getVars(self):
    return Object.get(self, '__variables__')

def getGeo(geometry):
    w, h, x, y = geometry
    return max(w, 0), max(h, 0), max(x, 0), max(y, 0)

def getTk(self):
    return Object.get(self, '__tk__')

def getTx(self):
    return Object.get(self, '__text__')

def AttrEvent(self, name, function):
    Object.get(self, '__on__')[name] = function

def setEvent(self, name, value):
    Object.set(self.event, name, value)

# status
def getStatus(self):
    return getData(self)['status']

def setStatus(self, status=None):
    data = getData(self)
    if status:
        if status != 'normal':
            data['-status'] = data['status']
        data['status'] = status
    elif data.get('-status'):
        data['status'] = data['-status']
        data['-status'] = None
