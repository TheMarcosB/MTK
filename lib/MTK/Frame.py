#############################################################
## Module  : GI.Interface.Frame ## Author   : Marcos Bento ##
## ---------------------------- ## ----------------------- ##
## Github  : TheMarcosBC        ## Twitter  : TheMarcosBC  ##
## ---------------------------- ## ----------------------- ##
## Facebook: TheMarcosBC        ## Instagram: TheMarcosBC  ##
#############################################################

# import local modules
from . import FrameCache, Variables
from .Get import *
from .. import Image
from ..Main import *

#############################################################
## ---------- here starts the module definitions --------- ##
#############################################################
# image
def frame(tag):
    vars = getVars(tag)
    check = FrameCache.getkeys('frame', vars.size, tag.style)
    if check != vars.check['frame']:
        vars.check['frame'] = check
        backgroundColor, borderColor = tag.style.backgroundColor,  tag.style.borderColor
        if backgroundColor != 'none' or borderColor != 'none':
            exists = FrameCache.get('frame', check)
            if exists:
                tkinter = exists[2]
            else:
                if backgroundColor == 'none': image = Image.new(vars.padsize)
                else: image = Image.new(vars.padsize, backgroundColor.rgba)
                image.corners(*tag.style.getValue('border-radius'))
                if borderColor != 'none': image.border(tag.style.borderWidth, borderColor.rgba, tag.style.borderStyle)
                tkinter = image.tkinter()
                FrameCache.set('frame', (check, image.size, tkinter))
            vars.canvas.itemconfig(vars['frame'], image=tkinter)
        else:
            vars.canvas.itemconfig(vars['frame'], image=None)

def background(tag):
    vars = getVars(tag)
    check = FrameCache.getkeys('background', vars.padsize, tag.style)
    if check != vars.check['background']:
        vars.check['background'] = check
        if tag.style.backgroundImage != 'none':
            exists = FrameCache.get('background', check)
            if exists:
                tkinter = exists[1]
            else:
                if isinstance(tag.style.backgroundImage, Variables.linear_gradient):
                    image = Image.new(vars.padsize)
                    image.linear_gradient(tag.style.backgroundImage, tag.style.backgroundImage.position)
                else:
                    image = tag.style.backgroundImage.content
                tkinter = image.tkinter()
                FrameCache.set('background', (check, image.size, tkinter))
            vars.canvas.itemconfig(vars['background'], image=tkinter)
        else:
            vars.canvas.itemconfig(vars['background'], image=None)

def image(tag):
    vars = getVars(tag)
    isicon = tag.realTag == 'icon'
    before = vars.check['image']
    if isicon: check = FrameCache.getkeys('icon', vars.padsize, tag.style)
    else: check = FrameCache.getkeys('image', vars.padsize, tag.style)
    if tag.style['-image'] != 'none':
        if isicon: exists = FrameCache.get('icon', check)
        else: exists = FrameCache.get('image', check)
        if exists:
            size = exists[1]
            tkinter = exists[2]
        else:
            image = tag.style['-image'].content.copy()
            image.corners(*tag.style.getValue('border-radius'))
            size, iconColor = image.size, tag.style.getParent('icon-color')
            if isicon and iconColor != 'none': image.color(iconColor)
            for key, value in tag.style['filter']: Object.attr(image, key)(value)
            tkinter = image.tkinter()
            if isicon: FrameCache.set('icon', (check, size, tkinter))
            else: FrameCache.set('image', (check, size, tkinter))
        if check != before:
            vars.check['image'] = check
            vars.canvas.itemconfig(vars['image'], image=tkinter)
        return size
    elif check != before:
        vars.check['image'] = check
        vars.canvas.itemconfig(vars['image'], image=None)

# tag
def hide(tag):
    vars = getVars(tag)
    vars.canvas.itemconfig(vars['shadow-outset'], state='hidden')
    vars.canvas.itemconfig(vars['frame'], state='hidden')
    vars.canvas.itemconfig(vars['background'], state='hidden')
    vars.canvas.itemconfig(vars['shadow-inset'], state='hidden')
    if vars.get('image'):
        vars.canvas.itemconfig(vars['image'], state='hidden')
    elif vars.get('text'):
        vars.canvas.itemconfig(vars['text-shadow'], state='hidden')
        vars.canvas.itemconfig(vars['text'], state='hidden')

def show(tag):
    vars = getVars(tag)
    vars.canvas.itemconfig(vars['shadow-outset'], state='normal')
    vars.canvas.itemconfig(vars['frame'], state='normal')
    vars.canvas.itemconfig(vars['background'], state='normal')
    vars.canvas.itemconfig(vars['shadow-inset'], state='normal')
    if vars.get('image'):
        vars.canvas.itemconfig(vars['image'], state='normal')
    elif vars.get('text'):
        vars.canvas.itemconfig(vars['text-shadow'], state='normal')
        vars.canvas.itemconfig(vars['text'], state='normal')

def position(tag, x, y):
    vars = getVars(tag)
    bd = tag.style['border-width']
    position = (bx, by) = x + bd[3], y + bd[0]
    vars.canvas.coords(vars['shadow-outset'], (x, y))
    vars.canvas.coords(vars['frame'], (x, y))
    vars.canvas.coords(vars['background'], position)
    vars.canvas.coords(vars['shadow-inset'], position)
    if vars.get('image'):
        vars.canvas.coords(vars['image'], position)
    elif vars.get('text'):
        shadowX, shadowY, *args = tag.style['text-shadow']
        vars.canvas.coords(vars['text-shadow'], bx + shadowX, by + shadowY)
        vars.canvas.coords(vars['text'], position)
    show(tag)

def display(tag, value):
    vars = getVars(tag)
    if vars.display != value:
        try:
            for item in tag.items:
                display(item, value)
        except:
            pass
        if vars.isdoc:
            tk = getTk(tag)
            if value: tk.configure(state='normal')
            else: tk.configure(state='disabled')
        else:
            if value: show(tag)
            else: hide(tag)
        vars.display = value

# update
def up(tag):
    frame(tag)
    background(tag)
