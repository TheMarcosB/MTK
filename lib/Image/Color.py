###################################################################
## Module  : Image.Color       ## Author   : Marcos Bento        ##
## --------------------------- ## ------------------------------ ##
## Github  : TheMarcosBC       ## Twitter  : TheMarcosBC         ##
## --------------------------- ## ------------------------------ ##
## Facebook: TheMarcosBC       ## Instagram: TheMarcosBC         ##
###################################################################

# import default modules
import math, os
from PIL import ImageColor

# import local modules
from ..Main import *

# fixed variables
Transparent = 127, 127, 127, 0

###################################################################
## ------------ here starts the module definitions ------------- ##
## start ##########################################################
def getrgba(value):
    if isinstance(value, (list, tuple)) and len(value) <= 4:
        new_color = []
        for i in range(4):
            try:
                val = value[i]
                if i == 3: new_color.append(getNum(math.floor(255 * val) if isinstance(val, float) else val, 0, 255))
                else: new_color.append(getNum(round(value[i]), 0, 255))
            except IndexError as error:
                if i == 3: new_color.append(255)
                else: raise ValueError
        return tuple(new_color)
    else:
        if value == 'transparent':
            return Transparent
        elif value[0] == '#':
            if len(value) == 4: return ImageColor.getrgb('#' + (value[1 : ] * 2)) + (255, )
            elif len(value) == 7: return ImageColor.getrgb(value) + (255, )
            else: return ImageColor.getrgb(value[ : 7]) + (getNum(int(value[8 : ], 16), 0, 255), )
        else:
            return ImageColor.getrgb(value) + (255, )

class new(tuple):
    # formats
    @property
    def hexa(self): return '#%02x%02x%02x%02x' % self.rgba

    @property
    def hex(self): return self.hexa[0 : 7]

    @property
    def rgb(self): return tuple(list(self.rgba)[0 : 3])

    # update
    def clear(self):
        self.rgba = tuple(self)

    def light(self, value):
        r, g, b, a = self
        if value < 0:
            r, g, b = round(r - (abs(value) * r)), round(g - (abs(value) * g)), round(b - (abs(value) * b))
        else:
            r, g, b = round(r + (value * (255 - r))), round(g + (value * (255 - g))), round(b + (value * (255 - b)))
        self.rgba = getNum(r, 0, 255), getNum(g, 0, 255), getNum(b, 0, 255), a
        return self

    def mix(self, color, value=0.5):
        color, rgb, value = new.__color__(color), (), getOne(value)
        for i in range(3): rgb += round(color[i] + (self[i] - color[i]) * value),
        self.rgba = rgb + (self[3], )
        return self

    def alpha(self, value):
        value = round(getOne(value) * 255)
        self.rgba = tuple(list(self)[0 : 3] + [value])
        return self

    # main
    def __color__(value):
        if isinstance(value, new):
            return value.rgba
        else:
            try: return getrgba(value)
            except: return Transparent

    def __new__(cls, value, iscolor=False):
        color = value if iscolor else new.__color__(value)
        self = tuple.__new__(cls, color)
        self.rgba = color
        return self

def getcolor(value):
    return new.__color__(value)

# end
setModule(__name__, '__call__', new)
