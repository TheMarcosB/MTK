#############################################################
## Module  : MTK.Variables      ## Author   : Marcos Bento ##
## ---------------------------- ## ----------------------- ##
## Github  : TheMarcosBC        ## Twitter  : TheMarcosBC  ##
## ---------------------------- ## ----------------------- ##
## Facebook: TheMarcosBC        ## Instagram: TheMarcosBC  ##
#############################################################

# import local modules
from .. import Image, Number, Path, String, Url
from ..Image import Color
from ..Main import *

# fixed variables
cache = {}

#############################################################
## ---------- here starts the module definitions --------- ##
#############################################################
# number
def percent(value):
    return Number.percent(value, ['%', 'l', 'h', 'w'])

def calc(value):
    return Number.inchcalc(value, 'px', False)

# color
def rgba(*values):
    return Color.new(values)

def rgb(*values):
    return Color.new(values)

def alpha(color, value):
    if not isinstance(color, Color.new): color = Color.new(color)
    color.alpha(value)
    return color

def light(color, value):
    if not isinstance(color, Color.new): color = Color.new(color)
    color.light(value)
    return color

def mix(self, color, value):
    if not isinstance(self, Color.new): self = Color.new(self)
    self.mix(color, value)
    return self

# image
class linear_gradient(tuple):
    def __new__(cls, value=None, *values):
        position = 'bottom'
        if value.replace('to ', '').strip() in ['top', 'right', 'bottom', 'left']: position = value.replace('to ', '').strip()
        else: values = (value, ) + values
        self = tuple.__new__(cls, values)
        self.position = position
        return self

class image(str):
    def __init__(self, path, type, data=None):
        content = Image.open(data if data else path)
        self.content = content
        cache[path] = self

    def __new__(cls, path, type, data=None):
        return str.__new__(cls, 'url(%s)' % path if type == 'url' else path)

# file
def file(path, type):
    typeof = String.typeof(path)
    if cache.get(path):
        return cache[path]
    else:
        if typeof == 'url':
            url = Url.open(path)
            if url.type == 'image': return image(path, type, url.bytes())
        elif Path.isfile(path):
            filetype =  Path.type(path)
            if filetype == 'image': return image(path, type)

def url(path):
    return file(path, 'url')

def src(path):
    return file(path, 'src')
