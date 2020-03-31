#########################################################
## Module  : MTK.Configure  ## Author   : Marcos Bento ##
## ------------------------ ## ----------------------- ##
## Github  : TheMarcosBC    ## Twitter  : TheMarcosBC  ##
## ------------------------ ## ----------------------- ##
## Facebook: TheMarcosBC    ## Instagram: TheMarcosBC  ##
#########################################################

# import local modules
from .Create import Body
from .Get import *
from ..Main import *

#########################################################
## -------- here starts the module definitions ------- ##
#########################################################
def border(window):
    bd, bg = window.configure.borderColor, window.configure.backgroundColor
    color = bd if bd != 'none' else bg
    getTk(window).configure(bg=color.hex if isinstance(color, tuple) else color)
    Body.resize(window)

def background(window, value):
    color = value.hex
    getTk(window).body.configure(bg=color)
    getTk(window.document.headerbar).configure(bg=color)
    getTk(window.document.buttons).configure(bg=color)

def opacity(window, value):
    getTk(window).attributes('-alpha', str(value))

def set(window, key, value):
    if key == 'background-color': background(window, value)
    elif key[ : 6] == 'border': border(window)
    elif key == 'opacity': opacity(window, value)
    elif key == 'padding': Body.resize(window)
