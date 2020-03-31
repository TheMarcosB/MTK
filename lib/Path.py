########################################################
## Module  : Path          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, os, re, sys

# import local modules
from . import Array, Number, Conf

# module variables
__call__ = 'about'
__tags__ = ['delete', 'dir', 'to', 'move', 'rename', 'file', 'split', 'bytes', 'read', 'length', 'size', 'mime', 'type', 'order', 'about', 'list']

# fixed variables
delete = os.remove
mkdir = os.mkdir
to = os.rename
exists = os.path.exists
isfile = os.path.isfile
isdir = os.path.isdir

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def move(path, directory):
    os.rename(path, directory + '/' + os.path.basename(path))

def rename(path, name):
    os.rename(path, os.path.dirname(path) + '/' + name)

def file(path):
   newfile = open(path, 'a')
   newfile.close()

def split(path):
    dirpath = os.path.dirname(path)
    dirname = os.path.basename(dirpath)
    filename = os.path.basename(path)
    if os.path.isdir(path):
        name = filename
        extension = 'x-directory'
    else:
        name, _extension = os.path.splitext(filename)
        if _extension != '': extension = _extension[1 : ].lower()
        else: extension = 'x-unknown'
    return name, extension, filename, dirname, dirpath

def bytes(path):
    devolve = b''
    if path and os.path.isfile(path):
        try: devolve = open(path, 'rb')
        except: pass
    return devolve

def read(path):
    devolve = ''
    if path and os.path.isfile(path):
        try: devolve = open(path, 'r')
        except: pass
    return devolve

def length(path):
    devolve = 0
    if os.path.isfile(path):
        try: devolve = os.path.getsize(path)
        except: pass
    return devolve

def size(path):
    return Number.byte(length(path))

def mime(path):
    try: return (Conf.sys('path-mimes') % split(path)[1])(0, 0)
    except: return 'application/octet-stream'

def type(path):
    try: return (Conf.sys('path-types') % split(path)[1])(0, 0)
    except: return 'other'

def order(path, istype=False):
    try:
        _type = type(path)
        _order = (Conf.sys('path-order') % _type)(0, 0)
        return (_order, _type) if istype else _order
    except:
        return ('x', 'other') if istype else 'x'

def about(path):
    name, extension, filename, dirname, dirpath = split(path)
    fileorder, filetype = order(path, True)
    return Array.new({
        'name': name,
        'extension': extension,
        'file': filename,
        'directory': dirname,
        'path': path,
        'mime': mime(path),
        'type': filetype,
        'order': fileorder,
        'size': size(path)
    })

def list(path, filter=False, ignore={}, local=''):
    keys = Array.keys(ignore)
    directory = sorted(os.listdir(path + '/' + local)) if path and os.path.isdir(path) else None
    files = Array.new()
    if directory and len(directory) > 0:
        for filename in directory:
            location = filename if local == '' else local + '/' + filename
            filepath = path + '/' + location
            check_dir = not filename in ignore['directory'] if os.path.isdir(filepath) and 'directory' in keys else True
            check_file = not filename in ignore['file'] if os.path.isfile(filepath) and 'file' in keys else True
            check_ext = not split(filepath)[1] in ignore['extension'] if 'extension' in keys else True
            check_hide = 'hidden' in keys and ignore['hidden'] == True if filename[0 : 1] == '.' else True
            if check_dir and check_file and check_ext and check_hide:
                _about = about(filepath)
                if _about:
                    _about['tags'] = local.split('/') if local else []
                    files += _about
                    if os.path.isdir(filepath) and filter:
                        Array.add(files, list(path, True, ignore, location))
    return files
