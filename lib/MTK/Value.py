########################################################
## Module  : MTK.Value     ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from . import Variables
from ..Main import *

########################################################
## ------- here starts the module definitions ------- ##
########################################################
style = {
    # frame
    'left': {'float': 'left'},
    'right': {'float': 'right'},
    'auto': {'float': '100l'}
}

def set(tag):
    if tag.tagName == 'button':
        count = len(tag.parents[0].getByTag('button'))
        tag.value = 'Button%s' % (count + 1) if count else 'Button'
    elif tag.tagName == 'select':
        count = len(tag.parents[0].getByTag('select'))
        tag.value = 'Select%s' % (count + 1) if count else 'Select'
    elif tag.tagName in ['check', 'radio', 'switch']:
        status = Paths.img, tag.tagName
        tag.style({'-image': Variables.url('%s/window/%s-off.png' % status)})
        tag.style.setHover({'-image': Variables.url('%s/window/%s-over-off.png' % status)})
        tag.style.setLocked({'-image': Variables.url('%s/window/%s-lock-off.png' % status)})
    if style.get(tag.tagName):
        tag.style.setDefault(style.get(tag.tagName))
