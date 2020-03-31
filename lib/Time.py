########################################################
## Module  : Time          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import time

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def real():
    return time.time()

def date():
    return time.strftime('%d/%m/%Y at %X')

def web():
    return time.strftime('%a, %d %b %Y %X %Z')
