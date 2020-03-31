#########################################################
## Module  : MTK.Update     ## Author   : Marcos Bento ##
## ------------------------ ## ----------------------- ##
## Github  : TheMarcosBC    ## Twitter  : TheMarcosBC  ##
## ------------------------ ## ----------------------- ##
## Facebook: TheMarcosBC    ## Instagram: TheMarcosBC  ##
#########################################################

# import default modules
import tkinter, time

# import local modules
from . import Frame, Tags
from .Get import *

#########################################################
## -------- here starts the module definitions ------- ##
#########################################################
# update
def _size(document, tag):
    style, vars = tag.style, getVars(tag)
    if vars.expand: width, height = vars.expand
    else: width, height = tag.style.getValue('size')
    if isinstance(tag, Tags.Label):
        text = getTx(tag)
        if 'auto' in [width, height]:
            if text.value != tag.value:
                w, h = text.clear()
            else:
                w, h = text.size
            if width == 'auto': width = w
            if height == 'auto': height = h
    elif isinstance(tag, Tags.Photo):
        imagesize = Frame.image(tag)
        if imagesize and width == 'auto': width = imagesize[0]
        if imagesize and height == 'auto': height = imagesize[1]
    issize = (isinstance(width, int) and width > 0) and isinstance(height, int) and height > 0
    if issize:
        if vars.insize != (width, height):
            vars.insize = width, height
            if vars.istk:
                if 'auto' in tag.style.size: vars.istk.configure(width=vars.w, height=vars.h)
                vars.istk.update()
    elif not issize:
        if vars.insize != (0, 0):
            vars.insize = 0, 0
            if vars.istk: vars.istk.configure(width=0, height=0)
            else: Frame.hide(tag)
    if vars.expand: vars.expand = False

def _position(document, tag):
    vars = getVars(tag)
    if vars.insize[0] > 0 and vars.insize[1] > 0:
        if tag.style.position in ['absolute', 'fixed']:
            if tag.style.position == 'fixed': w, h, x, y = document.getsize + (0, 0)
            else: w, h, x, y = vars.parent.padsize + (vars.parent.bx, vars.parent.by)
            top, right, bottom, left = tag.style.getValue('position-items')
            marginTop, marginRight, marginBottom, marginLeft = tag.style.getValue('margin')
            if right != 'none' and left != 'none':
                fx = left + marginLeft
                vars.x = x + fx
                vars.expand = w - (fx + right + marginRight), vars.getsize[0]
            elif right != 'none':
                vars.x = x + (w - (right + marginRight + vars.w))
            elif left != 'none':
                vars.x = x + left + marginLeft
            if top != 'none' and bottom != 'none':
                fy = top + marginTop
                vars.y = y + fy
                if vars.expand: vars.expand = vars.expand[0], h - (fx + bottom + marginBottom)
                else: vars.expand = vars.getsize[0], h - (fx + bottom + marginBottom)
            elif top != 'none':
                vars.y = y + top + marginTop
            elif bottom != 'none':
                vars.y = y + (h - (bottom + marginBottom + vars.h))
        else:
            width, height = vars.parent.getsize
            marginTop, marginRight, marginBottom, marginLeft = tag.style.getValue('margin')
            w, h = vars.w + marginRight + marginLeft, vars.h + marginTop + marginBottom
            float = tag.style.float
            if float in ['left', 'right']:
                auto = not isinstance(tag.parent, Tags.Document) and tag.parent.style.width == 'auto'
                if auto or width - (vars.parent.length + w) >= 0:
                    if float == 'right':
                        vars.x = width - (vars.parent.right + vars.w + marginRight)
                        vars.parent.right += w
                    else:
                        vars.x = vars.parent.left + marginLeft
                        vars.parent.left += w
                    if h > vars.parent.end: vars.parent.end = h
                    vars.parent.length += w
                else:
                    vars.parent.top += vars.parent.end
                    if float == 'right':
                        vars.x = width - (vars.w + marginRight)
                        vars.parent.left, vars.parent.right = 0, w
                    else:
                        vars.x = marginLeft
                        vars.parent.left, vars.parent.right = w, 0
                    vars.parent.length = w
                    vars.parent.end = h
                vars.y = vars.parent.top + marginTop
                if vars.parent.length > vars.parent.width: vars.parent.width = vars.parent.length
            else:
                isend = not (vars.parent.left == 0 and vars.parent.right > 0 and width - vars.parent.length >= w)
                if isend: vars.parent.top += vars.parent.end
                vars.x = marginLeft
                vars.y = vars.parent.top + marginTop
                if width - w <= 0:
                    vars.parent.end, vars.parent.left, vars.parent.length, vars.parent.right = 0, 0, 0, 0
                    vars.parent.top += h
                else:
                    vars.parent.left, vars.parent.length, vars.parent.right = w, w, 0
                    vars.parent.right = 0
                    if isend or (not isend and h > vars.parent.end): vars.parent.end = h
                if w > vars.parent.width: vars.parent.width = w
            vars.x = vars.parent.moveX + vars.parent.scrollX + vars.parent.px + vars.x
            vars.y = vars.parent.moveY + vars.parent.scrollY + vars.parent.py + vars.y
        if vars.position != (vars.x, vars.y):
            vars.position = vars.x, vars.y
            if not vars.istk or not isinstance(vars.istk, tkinter.Frame):
                if not getData(vars.window).get('update-loop') or vars.canvas != getTk(vars.document.buttons):
                    pd = document.window.configure.padding + document.window.configure.borderWidth
                    x, y = max(vars.canvas.winfo_x() - pd, 0), max(vars.canvas.winfo_y() - pd, 0)
                    Frame.position(tag, vars.x - x, vars.y - y)

def _configure(document, tag):
    vars = getVars(tag)
    if vars.insize[0] > 0 and vars.insize[1] > 0:
        Frame.up(tag)
        if isinstance(tag, (Tags.Label, Tags.Edit)):
            getTx(tag).up()

def _items(document, tag):
    vars = getVars(tag)
    vars.clear()
    if isinstance(tag, Tags.Frame) and 'auto' in tag.style.size:
        size = tag.style.getValue('size')
        for item in tag.items:_items(document, item)
        if size == ('auto', 'auto'): vars.expand = vars.width, vars.top + vars.end
        elif size[0] == 'auto': vars.expand = vars.width, size[1]
        else: vars.expand = size[0], vars.top + vars.end
        _size(document, tag)
        _position(document, tag)
        if not vars.istk or isinstance(vars.istk, tkinter.Canvas):
            _configure(document, tag)
    else:
        _size(document, tag)
        _position(document, tag)
        if not vars.istk or isinstance(vars.istk, tkinter.Canvas):
            _configure(document, tag)
        if isinstance(tag, Tags.Frame):
            for item in tag.items: _items(document, item)

def up(window):
    document = window.document
    vars = getVars(document)
    vars.clear()
    for tag in document.items:
        if tag.style.display != 'none': _items(vars, tag)
        else: Frame.display(tag, 0)
