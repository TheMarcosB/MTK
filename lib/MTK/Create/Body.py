########################################################
## Module  : MTK.Body      ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, time, tkinter

# import local modules
from ..Get import *
from ..Variables import *
from ... import Paths
from ...Main import *

# fixed variables
iconstyle = {
    'size': 16,
    'float': 'left',
    'padding': (0, 5),
    'margin': (3, 0, 0 , 10)
}

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# headerbar
def event_corner(window, data, tk, x, y, px, py, sw, sh):
    corner, (mx, mh, mx, my) = None, window.maxgeo
    if (px, py) == (0, 0): corner = 'top+left'
    elif (px + 1, py) == (sw, 0): corner = 'top+right'
    elif (px + 1, py + 1) == (sw, sh): corner = 'bottom+right'
    elif (px, py + 1) == (0, sh): corner = 'bottom+left'
    elif py <= my: corner = 'maximize'
    elif px + 1 == sw: corner = 'right'
    elif px == 0: corner = 'left'
    if not data.get('headerbar-geometry'):
        if corner:
            data['headerbar-corner'] = corner
            data['headerbar-geometry'] = window.geometry()
        if corner == 'maximize':
            window.maximize()
        elif corner in ['right', 'left']:
            w = math.floor(sw / 2)
            x = w if corner == 'right' else 0
            setStatus(window, corner)
            window.geometry(w, sh, x, 0)
    return corner

def event_click(event):
    data, tk = getData(event.window), getTk(event.window)
    data['headerbar-move'] = None
    data['headerbar-time'] = None
    tk.configure(cursor='arrow')

def event_press(event):
    data, tk = getData(event.window), getTk(event.window)
    data['headerbar-move'] = event.window_x, event.window_y
    data['headerbar-time'] = time.time()
    tk.configure(cursor='fleur')

def event_move(event):
    data, window = getData(event.window), event.window
    move, resize = data.get('headerbar-move'), data.get('corner-resize')
    if isinstance(move, tuple) and not resize and data['status'] != 'fullscreen':
        if time.time() - data['headerbar-time'] > 0.1:
            doc = event.document
            tk, btk1, btk2, htk = getTk(window), getTk(doc.buttons), getTk(doc.body), getTk(doc.headerbar)
            w, h, gx, gy = window.geometry()
            (x, y), (px, py), (sw, sh) = move, window.pointer, window.screensize
            corner = event_corner(window, data, tk, x, y, px, py, sw, sh)
            if corner or data.get('headerbar-geometry'):
                if not corner:
                    if data.get('headerbar-corner') == 'maximize':
                        window.maximize(geometry=data['headerbar-geometry'])
                    else:
                        window.geometry(*data['headerbar-geometry'])
                    data['headerbar-corner'] = data['headerbar-geometry'] = None
            elif (px - x) + w > sw or x > px:
                if not data.get('update-move') or time.time() - data['update-move'] > 0.03:
                    if (px - x) + w > sw:
                        geometry = getGeo((sw - (px - x), h, px - x, py - y))
                    else:
                        geometry = getGeo((px + (w - x), h, 0, py - y))
                        less = w - geometry[0]
                        btk1.place(x=(math.floor(w - 108)) - less)
                        btk2.place(x=5 - less)
                        htk.place(x=5 - less)
                    tk.geometry('%sx%s+%s+%s' % geometry)
                    data['update-move'] = time.time()
            elif not data.get('update-move') or time.time() - data['update-move'] > 0.01:
                window.geometry(w, h, px - x, py - y)
                data['update-move'] = time.time()
            data['update-time'] = time.time()

def resize(window):
    bd = window.configure.borderWidth
    pd = window.configure.padding + bd
    bd2, pd2 = bd * 2, pd * 2
    doc, (gw, gh, gx, gy) = window.document, window.geometry()
    isnormal = getData(window)['type'] == 'normal'
    # tags
    if isnormal:
        buttons, header, body = doc.buttons, doc.headerbar, doc.body
        buttonsW = buttons.style.width
        buttonsH, headerH = buttons.style.height, header.style.height
    else:
        body = doc.body
    # tkinter
    if bd > 0: getTk(window).body.place(width=gw - bd2, height=gh - bd2, x=bd, y=bd)
    if isnormal:
        buttonsTk, headerTK, bodyTK = getTk(buttons), getTk(header), getTk(body)
        buttonsTk.place(width=buttonsW, height=buttonsH, x=math.floor(gw - (buttonsW + pd)), y=pd)
        headerTK.place(width=math.floor(gw - pd2), height=headerH, x=pd, y=pd)
        bodyTK.place(width=math.floor(gw - pd2), height=math.floor(gh - (headerH + pd2)), x=pd, y=headerH + pd)
    else:
        getTk(doc.body).place(width=math.floor(gw - pd2), height=math.floor(gh - pd2), x=pd, y=pd)

def create(document, type):
    tk = getTk(document)
    configure = {'bd':0, 'highlightthickness':0}
    main = tkinter.Label(tk, bg='#cfcfcf')
    main.pack(expand=True, fill='both')
    tk.body = main
    if type == 'normal':
        # tkinter
        headertk = tkinter.Canvas(tk)
        headertk.configure(**configure, bg='#cfcfcf')
        # body tk
        bodytk = tkinter.Canvas(tk)
        bodytk.configure(**configure, bg='white')
        # buttons tk
        buttonstk = tkinter.Canvas(tk)
        buttonstk.configure(**configure, bg='#cfcfcf')
        # buttons tags
        buttons = document.createTag(('buttons', buttonstk))
        minimize = buttons.createTag('minimize', 'icon')
        maximize = buttons.createTag('maximize', 'icon')
        close = buttons.createTag('close', 'icon')
        # headerbar tags
        headerbar = document.createTag(('headerbar', headertk))
        about = headerbar.createTag('about', 'icon')
        title = headerbar.createTag('title')
        title.value = document.window.title
        # body tags
        body = document.createTag(('body', bodytk))
        # buttons events
        minimize.addEvent('click', document.window.minimize)
        maximize.addEvent('click', document.window.maximize)
        close.addEvent('click', document.window.close)
        # headerbar events
        headerbar.addEvent('press', event_press)
        document.window.addEvent('click', event_click)
        document.window.addEvent('cursor', event_move)
        # buttons style
        minimize.style.setDefault(iconstyle)
        maximize.style.setDefault(iconstyle)
        close.style.setDefault(iconstyle)
        buttons.style.setDefault({
            'width': 108,
            'height': 22,
            'position': 'fixed',
            'right': 0,
        })
        # headerbar style
        headerbar.style.setDefault(width='100%', height=27)
        about.style.setDefault(iconstyle, margin=(3, 0), padding=0)
        title.style.setDefault({
            'height': 22,
            'line-height': 22,
            'font-size': 15,
            'font-weight': 'bold',
            'float': 'left',
            'margin-left': 5,
            'relative': 'on'
        })
        # body style
        body.style.setDefault(width='100%', height=calc('100% - 27px'))
        # images
        for name in ['about', 'close', 'maximize', 'minimize']:
            locals()[name].src = '%s/window/%s.png' % (Paths.img, name)
        # add
        Object.set(document, 'buttons', buttons)
        Object.set(document, 'headerbar', headerbar)
        Object.set(document, 'title', title)
    else:
        bodytk = tkinter.Canvas(tk)
        bodytk.configure(**configure, bg='white')
        body = document.createTag(('body', bodytk))
        body.style.setDefault(width='100%', height='100%')
    Object.set(document, 'body', body)
    resize(document.window)
    if type == 'normal': document.window.configure(padding=5)
    document.window.configure(border=(1, 'solid', '#afafaf'))
