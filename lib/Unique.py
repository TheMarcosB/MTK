########################################################
## Module  : Unique        ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import hashlib, time

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def md5(string):
    return hashlib.md5(string.encode('ISO-8859-1')).hexdigest()

# sha
def sha1(string):
    return hashlib.sha1(string.encode('ISO-8859-1')).hexdigest()

def sha224(string):
    return hashlib.sha224(string.encode('ISO-8859-1')).hexdigest()

def sha256(string):
    return hashlib.sha256(string.encode('ISO-8859-1')).hexdigest()

def sha384(string):
    return hashlib.sha384(string.encode('ISO-8859-1')).hexdigest()

def sha512(string):
    return hashlib.sha512(string.encode('ISO-8859-1')).hexdigest()

# create unique id
def id():
    return md5(str(time.time()))
