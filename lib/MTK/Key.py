#########################################################
## Module  : MTK.Key        ## Author   : Marcos Bento ##
## ------------------------ ## ----------------------- ##
## Github  : TheMarcosBC    ## Twitter  : TheMarcosBC  ##
## ------------------------ ## ----------------------- ##
## Facebook: TheMarcosBC    ## Instagram: TheMarcosBC  ##
#########################################################

# import default modules
import math

# import local modules
from .Get import *
from ..Main import *

#########################################################
## ------- here starts the module definitions -------- ##
#########################################################
# edit
def charbar(tag, line, w, y, length, li, lx, index, isline):
    text, vars = getTx(tag), getVars(tag)
    data, pd = text.lines[index - 1], tag.style.padding
    if text.event == 'backscape':
        if li > 0:
            if tag.style.textAlign == 'left':
                if vars.scrollX < 0:
                    vars.scrollX += w
                text.bar =  pd[3] + lx, pd[0] + y
            else:
                if vars.scrollX < 0 and tag.style.textAlign == 'center':
                    vars.scrollX += bar[-1][1]
                text.bar = lx + pd[3], y + pd[0]
            data[0] = line[ : li - 1] + line[li : ]
        elif y > 0:
            prevLine = text.lines[index - 1]
            if tag.style['text-align'] == 'right':
                x = (prevLine[1][0] + prevLine[2]) - length
            elif tag.style['text-align'] == 'center':
                x = prevLine[2] + ((vars.size[0] - (length + prevLine[2])) / 2)
            else:
                x = prevLine[1][0] + prevLine[2]
            text.bar = x + pd[3], (y + pd[0]) - text.font.fonth
            data[3] = False
    elif text.event == 'delete':
        if vars.scrollX > bx and tag.style['text-align'] == 'right':
            vars.scrollX -= w
        elif lx < 0 and length > vars.size[0] and tag.style['text-align'] == 'center':
            vars.scrollX -= w
        if isline and len(text.lines) - 1 > index:
            nextLine = text.lines[index + 1]
            if isline:
                if tag.style['text-align'] == 'right':
                    x = lx - nextLine[2]
                elif tag.style['text-align'] == 'center':
                    x = length + ((vars.size[0] - (length + nextLine[2])) / 2)
                else:
                    x = bx
                text.bar = x + pd[3], y + pd[0]
                text.lines[index][-1] = False
            else:
                nextLine[0] = nextLine[0][1 : ]
        else:
            if tag.style['text-align'] == 'right':
                text.bar = bx + pd[3] + w, y + pd[0]
            elif lx > 0 and tag.style['text-align'] == 'center':
                text.bar = bx + pd[3] + w, y + pd[0]
                if length > vars.size[0]: vars.scrollX += w
            data[0] = line[ : li] + line[li + 1: ]
    elif text.event == 'paste':
        if li == 0: line = text.key + line
        elif li + 1 == len(line): line += text.key
        else: line =  line[ : li] + text.key + line[li : ]
        data[0] = line
        tw, th = text.getsize(text.key)
        text.bar = pd[3] + lx + tw, pd[0] + y + (tw - text.font.fonth)
    elif li > 0 and text.event == 'move' and text.key == 'left':
        text.bar = bar[-1][2] + pd[3], y + pd[0]
    elif text.event == 'move' and text.key == 'right':
        text.bar = lx + pd[3], y + pd[0]

def edit(tag):
    vars, text = getVars(tag), getTx(tag)
    if text.event != None and text.key != None:
        index, pd = 0, list(tag.style.padding)
        if tag.style['text-align'] == 'right': pd[3] = -pd[1]
        elif tag.style['text-align'] == 'center': pd[3] = 0
        if text.bar:
            if text.lines and not tag.value: text.lines.clear()
            if not text.lines:
                if text.event == 'paste' and text.key:
                    tag.value = text.key
                    text.up()
            else:
                width, height = text.size
                by = min(max(text.bar[1] - pd[0], 0), max(height - text.font.fonth, 0))
                if tag.style.textAlign in ['center', 'right']: bx = text.bar[0] - pd[3]
                else: bx = max(text.bar[0] - pd[3], 0)
                if text.bar[1] > height: bx = width
                if text.event == 'move':
                    if text.add == 'down': by = min(by + text.font.fonth, height)
                    elif text.add == 'up': by = max(by - text.font.fonth, 0)
                for string, (x, y), length, isline in text.lines:
                    if y > by - text.font.fonth:
                        li, lx, bx, by = 0, x, min(bx, x + length), None
                        for char in string:
                            w = text.font.charsize(char)[0]
                            if bx != None and lx > bx - (w / 1.5):
                                charbar(tag, string, w, y, length, li, lx, index, isline)
                                bx = None
                            lx += w
                            li += 1
                        if bx != None:
                            charbar(tag, string, 0, y, length, li - 1, lx, index, isline)
                        break
                    index += 1
        if text.lines and text.event in ['backscape', 'delete', 'paste'] and (text.bar or text.selects):
            newText = ''
            for line, position, length, isline in text.lines:
                newText += line
                if isline: newText += '\n'
            tag.value = newText
        text.event, text.key = None, None
        text.up()
        vars.canvas.update()

# events
def eventpress(event):
    pass

def eventclick(event):
    tag = event.widget
    text = getTx(tag)
    text.bar = event.x, event.y

def eventkey(event):
    key, tag = event.keysym.lower(),  event.widget
    text = getTx(tag)
    text.event, text.key = None, None
    if key in ['backspace', 'delete']:
        text.event = key
    elif key in ['right', 'left', 'down', 'up']:
        text.event, text.key = 'move', key
    elif key in ['<control_l+a>', '<control_r+a>']:
        text.event = 'select-all'
    elif key in ['<control_l+c>', '<control_r+c>']:
        text.event = 'copy'
    elif key in ['<control_l+v>', '<control_r+v>']:
        text.event, text.key = 'paste', getTk(event.window).clipboard_get()
    elif key in ['<control_l+x>', '<control_r+x>']:
        text.event = 'cut'
    elif key in ['<control_l+z>', '<control_r+z>'] and textIndex > 0:
        text.event = 'undo'
    elif key in ['<control_l+shift_l+z>', '<control_r+shift_l+z>'] and len(textItems) - 1 > textIndex:
        text.event = 'remake'
    elif key in ['return', 'kp_enter']:
        text.event, self.key = 'paste', '\n'
    elif event.char != '' and event.char == chr(event.keysym_num):
        text.event, text.key = 'paste', event.char
    if text.event != None: edit(tag)
