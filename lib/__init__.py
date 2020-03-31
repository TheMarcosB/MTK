########################################################
## Module  : Init          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import os, sys

########################################################
## ------- here starts the module definitions ------- ##
########################################################
_file = os.path.realpath(__file__)
_dir = os.path.dirname(_file)
_python = os.path.realpath('%s/../pylib' % (_dir))
sys.path.append(_python)
