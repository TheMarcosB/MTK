########################################################
## Module  : Variables     ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import os

# import local modules
from .  import Array, Code, Unique, Url

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def new():
    vars = {
        'Array': Array,
        'Number': Number,
        'String': String,
        'Sys': Sys,
        'Time': Time,
        'Url', Url
    }
    # coding
    vars['json_decode'] = Code.json_decode
    vars['json_encode'] = Code.json_encode
    vars['base64_decode'] = Code.base64_decode
    vars['base64_encode'] = Code.base64_encode
    vars['bin2hex'] = Code.bin2hex
    vars['hex2bin'] = Code.hex2bin
    vars['url_decode'] = Code.url_decode
    vars['url_encode'] = Code.url_encode
    # unique
    vars['md5'] = Unique.md5
    vars['sha1'] = Unique.sha1
    vars['sha224'] = Unique.sha224
    vars['sha256'] = Unique.sha256
    vars['sha384'] = Unique.sha384
    vars['sha512'] = Unique.sha512
    vars['Id'] = Unique.id
    # database
    vars['MarcosDB'] = None
    vars['FileDB'] = None
    # file
    vars['dirname'] = os.path.dirname
    vars['fileabout'] = Path.about
    vars['filebytes'] = Path.bytes
    vars['filemime'] = Path.mime
    vars['filesize'] = Path.size
    vars['filetype'] = Path.type
    vars['fileread'] = Path.read
    vars['isdir'] = os.path.isdir
    vars['isfile'] = os.path.isfile
    vars['ispath'] = os.path.exists
    # url
    vars['urlhead'] = Url.header
    vars['urlread'] = Url.content
    # marks
    return vars
