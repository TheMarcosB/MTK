#############################################################
## Module  : MTK.FrameCache     ## Author   : Marcos Bento ##
## ---------------------------- ## ----------------------- ##
## Github  : TheMarcosBC        ## Twitter  : TheMarcosBC  ##
## ---------------------------- ## ----------------------- ##
## Facebook: TheMarcosBC        ## Instagram: TheMarcosBC  ##
#############################################################

# fixed variables
cache = {
    'frame': [],
    'background': [],
    'image': [],
    'icon': []
}
keys = {
    'frame' : [
        'background-color',
        'border',
        'border-radius',
    ],
    'background': [
        'background-filter',
        'background-image',
        'background-position',
        'background-size',
        'border-radius',
    ],
    'icon': [
        'icon-color',
        'filter',
        '-image',
        'object-fit',
        'object-position',
        'border-radius',
    ],
    'image': [
        'filter',
        '-image',
        'object-fit',
        'object-position',
        'border-radius',
    ],
    'text': [
        'color',
        'font-type',
        'font-name',
        'font-size',
        'font-style',
        'font-weight',
        'line-height',
        'letter-spacing',
        'text-align',
        'text-decoration',
        'text-shadow',
        'word-break',
        'word-spacing',
    ]
}

#############################################################
## ---------- here starts the module definitions --------- ##
#############################################################
def getkeys(type, size, style):
    devolve = {'size': size}
    for key in keys[type]:
        if type == 'text' or (type == 'icon' and key == 'icon-color'):
            devolve[key] = style.getParent(key)
        else:
            devolve[key] = style.getValue(key)
    return devolve

def get(type, style):
    for items in cache[type]:
        _style, *args = items
        if _style == style: return items

def set(type, items):
    cache[type].append(items)
