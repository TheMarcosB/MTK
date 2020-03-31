########################################################
## Module  : MTK.Select    ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math

# import local modules
from ..Get import *
from ...Main import *

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def event_value(event):
    body, widget, window = event.document.body, event.widget, event.window
    for tag in window.widget.items:
        tag.selected = 'on' if tag == widget.item else 'off'
    window.widget.value = widget.value
    getData(window.parent)['popup'] = None
    window.close()

def create(event):
    widget, window = event.widget, event.window
    items, data = widget.items, getData(window)
    if widget != data.get('popup') and len(items) > 0:
        data['popup'] = widget
        vars = getVars(widget)
        if vars.name == None: vars.name = widget.value
        (w, h), (x, y), (gx, gy) = vars.size, vars.position, window.position
        (sw, sh), (tw, th) = window.screensize, getTx(widget).getsize(vars.name)
        pd = window.configure.padding + window.configure.borderWidth
        for tag in items:
            gtw, gth = getTx(widget).getsize(tag.value)
            if gtw > tw: tw = gtw
            th += gth
        tw, th = tw + 2, th + 2
        if tw > sw: tw = math.floor(sw / 2)
        if gx + pd + x + tw > sw: tx = (gx + pd + x + w) - tw
        else: tx = gx + pd + x
        if th > sh:
            th, ty = sh, 0
        else:
            if gy + pd + y + th > sh: ty = (gy + pd + y + h) - th
            else: ty = gy + pd + y
        popup = window.popup(tw, th, tx, ty)
        Object.set(popup, 'parent', window)
        Object.set(popup, 'widget', widget)
        body = popup.document.body
        none = body.createTag('item', 'label')
        none.value = vars.name
        none.addEvent('click', event_value)
        for tag in items:
            label = body.createTag('item', 'label')
            label.value = tag.value
            label.addEvent('click', event_value)
            Object.set(label, 'item', tag)
    else:
        data['popup'] = None
