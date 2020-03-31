#########################################################
## Module  : MTK.Default    ## Author   : Marcos Bento ##
## ------------------------ ## ----------------------- ##
## Github  : TheMarcosBC    ## Twitter  : TheMarcosBC  ##
## ------------------------ ## ----------------------- ##
## Facebook: TheMarcosBC    ## Instagram: TheMarcosBC  ##
#########################################################

# import default modules
import math, time

# import local modules
from . import Frame, Variables
from .Get import *
from ..Main import *

# fixed variables

#########################################################
## -------- here starts the module definitions ------- ##
#########################################################
# window
def window_click(event):
    getData(event.window)['corner-resize'] = None

def window_press(event):
    data = getData(event.window)
    data['corner-resize'] = data['corner-get']

def window_resize(event):
    data, window = getData(event.window), event.window
    if data['status'] == 'normal':
        corner = data.get('corner-resize')
        if corner:
            px, py = window.pointer
            geometry = list(window.geometry())
            x, y = geometry[2 : ]
            if corner in ['top', 'top+right', 'top+left']:
                geometry[1], geometry[3] = data['corner-y'] - py, py
            elif corner in ['bottom', 'bottom+right', 'bottom+left']:
                geometry[1] = py - y
            if corner in ['right', 'top+right', 'bottom+right']:
                geometry[0] = px - x
            elif corner in ['left', 'top+left', 'bottom+left']:
                geometry[0], geometry[2] = data['corner-x'] - px, px
            if not data.get('update-resize') or time.time() - data['update-resize'] > 0.05:
                window.geometry(*geometry)
                data['update-resize'] = time.time()
            setEvent(window, 'relative', False)
            data['update-time'] = time.time()
        else:
            getcorner, pointer, tk = '', None, getTk(window)
            pd = window.configure.padding + window.configure.borderWidth
            if event.window_y <= pd:
                getcorner += 'top'
                data['corner-y'] = window.height + window.y
            elif event.window_y >= window.height - pd:
                getcorner += 'bottom'
            if event.window_x <= pd:
                getcorner = '%s+left' % getcorner if getcorner else 'left'
                data['corner-x'] = window.width + window.x
            elif event.window_x >= window.width - pd:
                getcorner = '%s+right' % getcorner if getcorner else 'right'
            if getcorner == 'top': pointer = 'top_side'
            elif getcorner == 'top+right': pointer = 'top_right_corner'
            elif getcorner == 'top+left': pointer = 'top_left_corner'
            elif getcorner == 'right': pointer = 'right_side'
            elif getcorner == 'bottom': pointer = 'bottom_side'
            elif getcorner == 'bottom+right': pointer = 'bottom_right_corner'
            elif getcorner == 'bottom+left': pointer = 'bottom_left_corner'
            elif getcorner == 'left': pointer = 'left_side'
            else: pointer = 'arrow'
            if tk['cursor'] != pointer and not data.get('headerbar-move'):
                tk.configure(cursor=pointer)
            data['corner-get'] = getcorner

# widget
def status_value(tag, value):
    status = Paths.img, tag.tagName, ('on' if value else 'off')
    tag.style({'-image': Variables.url('%s/window/%s-%s.png' % status)})
    tag.style.setHover({'-image': Variables.url('%s/window/%s-over-%s.png' % status)})
    tag.style.setLocked({'-image': Variables.url('%s/window/%s-lock-%s.png' % status)})
    return 1 if value else 0

def status_event(event):
    tag = event.widget
    value = tag.value
    tag.value = 0 if value else 1
