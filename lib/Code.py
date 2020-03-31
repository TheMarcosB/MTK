########################################################
## Module  : Code          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import base64, json, re

# import local modules
from . import Array

########################################################
## ------- here starts the module definitions ------- ##
########################################################

# json
def json_decode(string):
    try: return Array.convert(json.loads(string))
    except: return Array.new()

def json_encode(array):
    try: return json.dumps(array)
    except: return ''

# base64
def base64_decode(string):
    return base64.b64decode(string.encode('ISO-8859-1')).decode('ISO-8859-1')

def base64_encode(string):
    return base64.b64encode(string.encode('ISO-8859-1')).decode('ISO-8859-1')

# hex and bytes
def bin2hex(string):
    return binascii.b2a_hex(string.encode('ISO-8859-1')).decode('ISO-8859-1')

def hex2bin(string):
    return binascii.a2b_hex(string.encode('ISO-8859-1')).decode('ISO-8859-1')

# quote
def url_decode(string, swap=None):
    if swap:
        swapped = Array.todict(swap)
        for i in swapped.keys():
            string = string.replace(i, swapped[i])
    for i in re.findall('(%[A-z0-9]{2})', string):
        try: string = string.replace(i, chr(int(i[1 : ], 16)))
        except: pass
    return string

def url_encode(string, swap=None, ignore=''):
    devolve = ''
    if swap: swapped = Array.todict(swap)
    for i in string:
        if swap and i in swapped.keys(): devolve += str(swapped[i])
        elif i.isalpha() or i.isdigit() or i in ignore: devolve += i
        else: devolve += '%' + hex(ord(i))[2 : ].upper()
    return devolve