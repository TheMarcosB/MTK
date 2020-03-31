#########################################################
## Module  : MTK.Text       ## Author   : Marcos Bento ##
## ------------------------ ## ----------------------- ##
## Github  : TheMarcosBC    ## Twitter  : TheMarcosBC  ##
## ------------------------ ## ----------------------- ##
## Facebook: TheMarcosBC    ## Instagram: TheMarcosBC  ##
#########################################################

# import default modules
import math
from PIL import Image, ImageFilter, ImageDraw, ImageTk

# import local modules
from . import FrameCache
from .Get import *
from ..Image import Font, Color
from ..Main import *

# fixed variables
styles = ['name', 'size', 'line-height', 'type', 'weight', 'style', 'letter-spacing']

#########################################################
## ------- here starts the module definitions -------- ##
#########################################################
def position(self, length):
    devolve, vars, align = 0, getVars(self.tag), self.style.getParent('text-align')
    if align == 'right': devolve = math.floor(vars.getsize[0] - length)
    elif align == 'center': devolve = math.floor((vars.getsize[0] - length) / 2)
    return devolve

def createline(self, line, length, y, isline=False):
    self.lines.append([line, (position(self, length), y), length, isline])

def reader(self):
    (width, height), index, y, h = getVars(self.tag).getsize, 0, 0, self.font.fonth
    for line in self.value.split('\n'):
        isline = index != self.value.count('\n')
        word_break = self.style.getParent('word-break')
        if line and word_break in ['break-all', 'keep-all']:
            countSpace, length, spaces, string = 1, 0, line.split(' '), ''
            for space in spaces:
                if countSpace != len(spaces): space += ' '
                if word_break == 'break-all':
                    charLength, charString= 0, ''
                    for char in space:
                        charSize = self.font.charsize(char)[0]
                        if charSize + charLength > width:
                            createline(self, charString, charLength, y)
                            charString, charLength = char, charSize
                            y += h
                        else:
                            charString += char
                            charLength += charSize
                else:
                    string, length = space, self.font.getsize(space)[0]
                if length + charLength > width:
                    createline(self, string, length, y)
                    string, length = charString, charLength
                    y += h
                else:
                    string += charString
                    length += charLength
                countSpace += 1
            if string:
                createline(self, string, length, y, isline)
                y += h
        else:
            createline(self, line, self.font.getsize(line)[0], y, isline)
            y += h
        index += 1

def argsv(style):
    items = []
    for i in styles:
        if i.count('-') > 0: items.append(style.getParent(i))
        else: items.append(style.getParent('font-%s' % i))
    return items

def getfont(self):
    return Font.get(*argsv(self.style))

class new:
    def getsize(self, value):
        return self.font.getsize(value)

    def clear(self):
        self.font, self.y = getfont(self), (0, 0)
        self.lines.clear()
        self.size = self.textsize = self.getsize(self.tag.value)
        return self.size

    def up(self):
        vars = getVars(self.tag)
        check = FrameCache.getkeys('text', vars.size, self.tag.style)
        if self.value != self.tag.value or check != vars.check['text']:
            self.value = self.tag.value
            vars.check['text'] = check
            if self.tag.value:
                if not self.textsize: self.clear()
                reader(self)
                blur, color = 0, Color.new(self.style.getParent('color'))
                size, x, y = vars.padsize, vars.scrollX, vars.scrollY
                # size
                (width, height), (pt, pr, pb, pl) = size, self.style['padding']
                # text
                textBg = Image.new('RGBA', size, Color.Transparent)
                textDraw = ImageDraw.Draw(textBg)
                # shadow
                shadowX, shadowY, blur, shadowColor = self.style.getParent('text-shadow')
                blur, shadowColor = max(blur, 0), Color.new(shadowColor)
                if shadowX != 0 or shadowY != 0 or blur > 0:
                    shadowBg = Image.new('RGBA', size, shadowColor.alpha(0).rgba)
                    shadowDraw = ImageDraw.Draw(shadowBg)
                else:
                    shadowBg = None
                # lines
                for line, (lx, ly), length, isline in self.lines:
                    lx += pl + x; ly += pt + y
                    if ly >= 0 and ly < height + self.font.fonth:
                        if line:
                            for char in line:
                                font = self.font.detect(char)
                                charSize = font.charsize(char)[0]
                                if lx + charSize >= 0 and lx <= width:
                                    if shadowBg: shadowDraw.text((lx, ly + font.chary(char)), char, shadowColor, font=font)
                                    textDraw.text((lx, ly + font.chary(char)), char, color, font=font)
                                lx += charSize
                # append
                self.text = ImageTk.PhotoImage(textBg)
                vars.canvas.itemconfig(vars['text'], image=self.text)
                if shadowBg:
                    if blur > 0: shadowBg = shadowBg.filter(ImageFilter.GaussianBlur(blur / 3))
                    self.shadow = ImageTk.PhotoImage(shadowBg)
                    vars.canvas.itemconfig(vars['text-shadow'], image=self.shadow)
                else:
                    vars.canvas.itemconfig(vars['text-shadow'], image=None)
            else:
                self.lines.clear()
                vars.canvas.itemconfig(vars['text'], image=None)
                vars.canvas.itemconfig(vars['text-shadow'], image=None)
            self.textsize = None

    def __init__(self, tag):
        self.tag, self.style, self.size = tag, tag.style, (0, 0)
        self.lines, self.value, self.textsize = [], None, None
        # key
        self.event, self.key = None, None
        self.bar, self.select, self.selects = None, '', []
        Object.set(tag, '__text__', self)
