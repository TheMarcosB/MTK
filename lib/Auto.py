########################################################
## Module  : Auto          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import os

# import local modules
from . import Json

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def exe(path):
    extension = os.path.splitext(path)[1].lower()
    print(extension)
    if extension == '.json': return Json.decode, Json.encode

def get(path):
    try: return exe(path)[0]
    except: None

def set(path):
    try: return exe(path)[1]
    except: None
