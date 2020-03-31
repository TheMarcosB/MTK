########################################################
## Module  : Image.Font    ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, os, PIL.ImageFont as Font

# import local modules
from .. import Array, Conf, Paths, String

# fixed variables
default = 'Noto'
detects = Conf.sys('font-detect')
fonts = {}

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def _get(family, size, height, type, weight, style, spacing, fontmain=True):
    fontkey, fontpath, s, t, w = None, None, style, type, weight
    local = Paths.etc.fonts[family] + '/'
    for t in [type.capitalize(), 'Serif', 'Sans', 'Mono', '']:
        for e in ['ttf', 'otf', 'ttc']:
            for s in ['-' + style.capitalize(), '']:
                if s != '-' and s != 'None':
                    fontweight = '%s%s-%s%s.%s' % (family, t, weight.capitalize(), s, e)
                    fontregular = '%s%s-Regular%s.%s' % (family, t, s, e)
                    if os.path.isfile(local + fontweight):
                        fontkey, fontpath, w = fontweight, local + fontweight, weight
                        break
                    elif os.path.isfile(local + fontregular):
                        fontkey, fontpath, w = fontregular, local + fontregular, 'regular'
                        break
                    if fontkey: break
                if fontkey: break
            if fontkey: break
        if fontkey: break
    fontget = '%s.%s' % (fontkey, size)
    if fonts.get(fontget):
        return fonts[fontget]
    else:

            try:
                info = Conf.open(local + 'info.conf')
                if Array.iskey(info, 'inherits'): t = info.inherits
            except:
                info = None
            fonts[fontget] = new(fontpath, family, size, height, t, w, s.replace('-', ''), spacing, info)
            return fonts[fontget]


class new(Font.FreeTypeFont):
    @property
    def support(self):
        info, type = self.data[7], '%s-support' % self.data[3].lower()
        if type and Array.iskey(info, type): support = info[type]
        else: support = info.support
        return support if isinstance(support, Array.new) else Array.new()

    @property
    def fonth(self):
        if isinstance(self.data[2], int): return self.data[2]
        else: return self.data[1] + math.floor((self.data[1] / 100) * 10)

    @property
    def fonty(self):
        if isinstance(self.data[2], int):
            try: return math.floor((self.fonth - self.data[1]) / 2)
            except: return 0
        else:
            return 0

    def detect(self, char):
        detect = String.charDetect(char)
        if Array.iskey(detects, detect) and not detect in self.support:
            return _get(detects[detect], *self.data[1 : -1])
        else:
            return self

    def chary(self, char):
        font = self.detect(char)
        top = font.data[7].top
        if not isinstance(top, int): top = font.data[7][font.data[3].lower() + '-top']
        if isinstance(top, int) and top != 0:
            if top > 0: return font.fonty + math.floor((font.data[1] / 100) * top)
            else: return font.fonty - math.floor((font.data[1] / 100) * abs(top))
        else:
            return font.fonty

    def charsize(self, char):
        font = self.detect(char)
        size = Font.FreeTypeFont.getsize(font, char)
        spacing = self.data[6] if isinstance(self.data[6], int) else 0
        return size[0] + spacing, size[1]

    def getsize(self, text):
        lines = text.split('\n')
        width, height = 0, 0
        for line in lines:
            if line != '':
                length = 0
                for char in line: length += self.charsize(char)[0]
                if length > width: width = length
            height += self.fonth
        return width, height

    def __init__(self, file, family, size, height, type, weight, style, spacing, info):
        Font.FreeTypeFont.__init__(self, file, size)
        self.data = [family, size, height, type, weight, style, spacing, info]

def get(family, size, height=0, type='serif', weight='regular', style='', spacing=0):
    return _get(family, size, height, type, weight, style, spacing)
