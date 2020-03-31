###########################################################
## Module  : MTK.Style        ## Author   : Marcos Bento ##
## -------------------------- ## ----------------------- ##
## Github  : TheMarcosBC      ## Twitter  : TheMarcosBC  ##
## -------------------------- ## ----------------------- ##
## Facebook: TheMarcosBC      ## Instagram: TheMarcosBC  ##
###########################################################

# import default modules
import math, re

# import local modules
from . import Configure, Variables
from .. import Array, Class, Number
from .Get import *
from ..Image import Color
from ..Main import *

# fixed variables
_float = float

###########################################################
## -------- here starts the module definitions --------- ##
###########################################################
# tags
class bass:
    def __init__(self, *argsv, **argsk):
        self.args = argsk.get('default')
        self.list = argsk.get('list')
        self.side = argsk.get('side')
        self.size = argsk.get('size')
        self.type = argsk.get('type', self.__class__.__name__)

class float(bass, _float):
    pass

class items(bass, tuple):
    def __new__(cls, *value, **argsk):
        return tuple.__new__(cls, value)

class number(bass, int):
    def __new__(cls, value, **argsk):
        return int.__new__(cls, value)

class string(bass, str):
    def __new__(cls, value='', **argsk):
        return str.__new__(cls, value)

# defaults
canvas = ['ellipse', 'image', 'line', 'rectangle', 'text']
filters = ['blur', 'brightness', 'contrast', 'grayscale', 'invert', 'opacity', 'saturate', 'sepia']
listx = ['top', 'center', 'bottom']
listy = ['right', 'center', 'left']
repeat = ['loop-round', 'loop-stretch', 'repeat', 'repeat-x', 'repeat-y', 'round', 'round-x', 'round-y']
size = ['contain', 'cover', 'fill']
none = ['none']
power = ['on', 'off']

# arguments
args = {
    # widget
    'size': items(string('width', type='link'), string('height', type='link'), type='complete'),
    'width': string('auto', list=['auto'], type='number', size='w', side='external'),
    'height': string('auto', list=['auto'], type='number', size='h', side='external'),
    'box-shadow': items(0, 0, 0, 0, string('none', type='color', list=none), string('outset', list=['inset', 'outset'])),
    'cursor': string('arrow'),
    'display': string('block', list=['block', 'none']),
    'float': string('none', list=['left', 'none', 'right']),
    'opacity': float(1.0),
    'relative': string('off', list=power),
    # background
    'background-attachment': string('scroll', list=['fixed', 'scroll']),
    'background-canvas': items(default=items(string(list=canvas), number(0, size='w', side='internal'), number(0, size='h', side='internal'), number(0, size='w', side='internal'), number(0, size='h', side='internal'), string('none', type='color', list=none)), type='append'),
    'background-color': string('none', type='color', list=none),
    'background-filter': items(default=items(string(list=filters), float(0.0)), type='append'),
    'background-image': string('none', type='image'),
    'background-repeat': string('no-repeat', list=repeat),
    'background-position': items(string('left', type='number', list=listx, size='w', side='internal'), string('top', type='number', list=listy, size='h', side='internal')),
    'background-size': items(string('auto', list=size, size='w', side='internal'), string('auto', list=size, size='h', side='internal')),
    # image
    '-image': string('none', type='image'),
    'icon-color': string('none', type='color', list=none),
    'filter': items(default=items(string(list=filters), float(0.0)), type='append'),
    'object-fit': string('contain', list=size),
    'object-position': items(string('left', list=listx, size='w', side='internal'), string('top', list=listy, size='h', side='internal')),
    # border
    'border': items(string('border-width', type='link'), string('border-style', type='link'), string('border-color', type='link'), type='links'),
    'border-color': string('none', type='color', list=none),
    'border-width': items(string('border-top', type='link'), string('border-right', type='link'), string('border-bottom', type='link'), string('border-left', type='link'), type='complete'),
    'border-style': string('solid', list=['solid', 'inbutton', 'outbutton', 'inset', 'outset']),
    'border-top': number(0),
    'border-right': number(0),
    'border-bottom': number(0),
    'border-left': number(0),
    # radius
    'border-radius': items(string('border-radius-top', type='link'), string('border-radius-right', type='link'), string('border-radius-bottom', type='link'), string('border-radius-left', type='link'), type='complete'),
    'border-radius-top': number(0, size='h', side='internal'),
    'border-radius-right': number(0, size='w', side='internal'),
    'border-radius-bottom': number(0, size='h', side='internal'),
    'border-radius-left': number(0, size='w', side='internal'),
    # font
    'font': items(string('font-family', type='link'), string('font-size', type='link'), type='links'),
    'font-family': items(string('font-name', type='link'), string('font-type', type='link'), type='links'),
    'font-type': string('serif'),
    'font-name': string('Noto'),
    'font-size': number(13, size='h', side='internal', list=none),
    'font-style': string('none', list=['italic', 'none', 'oblique']),
    'font-weight': string('none', list=['bold', 'none', 'normal']),
    # text
    'color': string('none', type='color', list=none),
    'line-height': string('none', size='h', side='internal', type='number', list=none),
    'letter-spacing': string('none', type='number', list=none),
    'text-align': string('none', list=listy),
    'text-decoration': string('none', list=['line-through', 'none', 'overline', 'underline']),
    'text-shadow': items(number(0), number(0), number(0), string('none', type='color', list=none)),
    'word-break': string('none', list=['break-all', 'keep-all', 'none']),
    'word-spacing': string('none', type='number', list=none),
    # margin
    'margin': items(string('margin-top', type='link'), string('margin-right', type='link'), string('margin-bottom', type='link'), string('margin-left', type='link'), type='complete'),
    'margin-top': number(0, size='h', side='external'),
    'margin-right': number(0, size='w', side='external', list=['auto']),
    'margin-bottom': number(0, size='h', side='external'),
    'margin-left': number(0, size='w', side='external', list=['auto']),
    # padding
    'padding': items(string('padding-top', type='link'), string('padding-right', type='link'), string('padding-bottom', type='link'), string('padding-left', type='link'), type='complete'),
    'padding-top': number(0),
    'padding-right': number(0),
    'padding-bottom': number(0),
    'padding-left': number(0),
    # position
    'position': string('none', list=['absolute', 'fixed', 'none']),
    'position-items': items(string('top', type='link'), string('right', type='link'), string('bottom', type='link'), string('left', type='link'), type='links'),
    'top': string('none', size='h', side='external', type='number', list=listy),
    'right': string('none', size='w', side='external', type='number', list=listx),
    'bottom': string('none', size='h', side='external', type='number', list=listy),
    'left': string('none', size='w', side='external', type='number', list=listx)
}
config_args = {
    # window
    'cursor': string('arrow'),
    'padding': number(0),
    'theme': string('none', list=none),
    'style': string('none', list=['dark', 'light', 'none']),
    # background
    'opacity': float(1.0),
    'background-color': string('#cfcfcf', type='color'),
    # radius
    'border-radius': items(string('border-radius-top', type='link'), string('border-radius-right', type='link'), string('border-radius-bottom', type='link'), string('border-radius-left', type='link'), type='complete'),
    'border-radius-top': number(0),
    'border-radius-right': number(0),
    'border-radius-bottom': number(0),
    'border-radius-left': number(0),
    # border
    'border': items(string('border-width', type='link'), string('border-style', type='link'), string('border-color', type='link'), type='links'),
    'border-color': string('none', type='color', list=none),
    'border-width': number(0),
    'border-style': string('solid', list=['solid', 'inbutton', 'outbutton', 'inset', 'outset']),
    # font
    'font': items(string('font-family', type='link'), string('font-size', type='link'), type='links'),
    'font-family': items(string('font-name', type='link'), string('font-type', type='link'), type='links'),
    'font-type': string('serif'),
    'font-name': string('Noto'),
    'font-size': number(13),
    'font-style': string('none', list=['italic', 'none', 'oblique']),
    'font-weight': string('none', list=['bold', 'none', 'normal']),
    # text
    'color': string('black', type='color', list=none),
    'line-height': string('none', size='h', side='internal', type='number', list=none),
    'letter-spacing': string('none', type='number', list=none),
    'text-align': string('none', list=listy),
    'text-decoration': string('none', list=['line-through', 'none', 'overline', 'underline']),
    'text-shadow': items(number(0), number(0), number(0), string('none', type='color', list=none)),
    'word-break': string('none', list=['break-all', 'keep-all', 'none']),
    'word-spacing': string('none', type='number', list=none),
}

# get style
def _get(self, key, isdefault=False):
    isconf = isinstance(self, config)
    default = (config_args if isconf else args)[key]
    if default.type == 'link':
        return _get(self, default, isdefault)
    elif default.type in ['append', 'complete', 'items', 'links']:
        count, items = 0, ()
        for d in default:
            if d.type == 'link':
                items += _get(self, d, isdefault),
            else:
                try:
                    v = Object.get(self, 'current')[key][count]
                except:
                    try:
                        if isconf:
                            v = Object.get(self, 'style')[key][count]
                        else:
                            try: v = Object.get(self, 'default')[key][count]
                            except: v = Object.get(self, 'style')[key][count]
                    except:
                        v = d
                items += ((d, v) if isdefault else v),
            count += 1
        return (default, items) if isdefault else items
    else:
        _style = Object.get(self, 'style').get(key, default)
        if isconf:
            _current = Object.get(self, 'current').get(key, _style)
        else:
            _default = Object.get(self, 'default').get(key, _style)
            _current = Object.get(self, 'current').get(key, _default)
        return (default, _current) if isdefault else _current

# set style
def _realcomplete(value):
    if isinstance(value, (list, tuple)):
        if len(value) == 2: return tuple(value * 2)
        elif len(value) == 3: return tuple(value) + (value[1], )
        else: return value
    else:
        return (value, ) * 4

def _token(string):
    try:
        value, *args = re.split('([^-\d.]+)', string)
        token = args[0] if len(args) > 0 else None
        float(value)
        if token in ['%', 'w', 'h', 'l', 't', 'pw', 'ph']: return 'percent', token
        elif token in Number._inchtypes.keys(): return 'inch', token
        elif not token: return 'string', ''
        else: return 'other', ''
    except:
        return 'other', ''

def _realvalue(default, value):
    if default.list and value in default.list:
        return value
    elif default.type == 'append':
        if isinstance(value, (list, tuple)):
            devolve = ()
            for v in value:
                item = _realvalue(default.args, v)
                if item != None: devolve += item,
            return devolve
    elif default.type == 'items':
        if isinstance(value, (list, tuple)) and len(default) == len(value):
            devolve = ()
            for d, v in zip(default, value):
                item = _realvalue(d, v)
                if item != None: devolve += item,
            if len(default) == len(devolve): return devolve
    elif default.type == 'color' and isinstance(value, (list, str, tuple)):
        if isinstance(value, Color.new):
            return value
        else:
            try: return Color.new(Color.getrgba(value), True)
            except: pass
    elif default.type == 'string' and default and isinstance(value, str):
        return value
    elif default.type == 'float' and isinstance(value, (_float, int, str)):
        return _float(value)
    elif default.type == 'image' and isinstance(value, Variables.image):
        return value
    elif default.type == 'number':
        if isinstance(value, str):
            type, token = _token(value)
            if type == 'percent' and default.size: return Number.percent(value, token)
            elif type == 'inch': return math.floor(Number.inch(value, 'px'))
            elif type == 'string': return math.floor(float(value))
        elif default.size and isinstance(value, (Number.inch, Number.percent)):
            return value
        elif isinstance(value, (float, int)):
            return math.floor(value)

def _set(self, key, value, status):
    isconf = isinstance(self, config)
    default = (config_args if isconf else args)[key]
    if default.type == 'link':
        _set(self, default, value, status)
    elif default.type == 'complete':
        items = _realcomplete(value)
        if items:
            for k, v in zip(default, items):
                _set(self, k, v, status)
    elif default.type == 'links':
        if isinstance(value, (list, tuple)) and len(default) == len(value):
            for k, v in zip(default, value):
                _set(self, k, v, status)
    else:
        v = value
        value = _realvalue(default, value)
        if value != None:
            before = self[key]
            Object.get(self, status)[key] = value
            if isconf and status == self.status and before != value:
                Configure.set(Object.get(self, 'window'), key, value)
        else:
            try: del Object.get(self, status)[key]
            except: pass

def _setitems(self, style, argsk, status):
    if Array.isadd(style):
        style = Array.todict(style).copy()
        style.update(argsk)
    else:
        style = argsk
    if style:
        for key, value in style.items():
            _set(self, key, value, status)
        if not status in ['locked', 'style'] and self.status == status:
            change(self, status)

def _realkey(key):
    devolve = ''
    for char in key:
        if char.isupper(): devolve += '-' + char.lower()
        else: devolve += char
    return devolve

# values
def _number(value, args):
    try:
        if args and isinstance(value, Number.inchcalc): return math.floor(value(args))
        elif args and isinstance(value, Number.percent): return math.floor(value(args[value.token]))
        elif isinstance(value, int): return value
        else: return 0
    except:
        return 0

def _corners(tag, vars, key, value):
    items = ()
    w, h = vars.getsize
    if w > h: args = {'l': 0, 'w': w, 'h': h, '%': w}
    else: args = {'l': 0, 'w': w, 'h': h, '%': h}
    for v in tag.style.borderRadius: items += _number(v, args),
    if key == 'border-radius-top': return items[0]
    if key == 'border-radius-right': return items[1]
    if key == 'border-radius-bottom': return items[2]
    if key == 'border-radius-left': return items[3]
    else: return items

def _margin(tag, vars, key, value):
    count, items, parent = 0, (), vars.parent
    args = {
        'w': {'l': parent.length, 'w': parent.w, 'h': parent.h, '%': parent.w},
        'h': {'l': parent.length, 'w': parent.w, 'h': parent.h, '%': parent.h}
    }
    for value in value if value != None else tag.style.margin:
        if count % 2 == 0:
            items += _number(value, args['h']),
        else:
            if value == 'auto':
                if vars.parent.isdoc or tag.parent.style.width != 'auto':
                    value = (parent.padsize[0] - vars.w) / 2
                else:
                    value = 0
            else:
                value = _number(value, args['w'])
            items += value,
        count += 1
    if key == 'margin-top': return items[0]
    if key == 'margin-right': return items[1]
    if key == 'margin-bottom': return items[2]
    if key == 'margin-left': return items[3]
    else: return items

def _args(tag, vars, default, value):
    if default.type == 'number' and value != 'auto':
        if default.side == 'internal':
            (w, h), (pw, ph) = vars.padsize, vars.getsize
            if default.size == 'w':
                return {'l': 0, 't': 0, 'w': w, 'h': h, 'pw': pw, 'ph': ph, '%': w}
            else:
                return {'l': 0, 't': 0, 'w': w, 'h': h, 'pw': pw, 'ph': ph, '%': h}
        else:
            (w, h), (pw, ph) = vars.parent.padsize, vars.parent.getsize
            if pw > vars.parent.length and tag.style.float != 'none': l = pw - vars.parent.length
            else: l = pw
            if ph > vars.parent.top and vars.parent.top > 0: t = ph - vars.parent.top
            else: t = ph
            if default.size == 'w':
                return {'l': l, 't': t, 'w': w, 'h': h, 'pw': pw, 'ph': ph, '%': w}
            else:
                return {'l': l, 't': t, 'w': w, 'h': h, 'pw': pw, 'ph': ph, '%': h}

def _value(tag, vars, default, value):
    if default.type in ['append', 'items']:
        values = ()
        for d, v in zip(default, value): values += _value(tag, vars, d, v),
        return values
    else:
        if default.type == 'number':
            try:
                args = _args(tag, vars, default, value)
                if args and isinstance(value, Number.inchcalc): return math.floor(value(args))
                elif args and isinstance(value, Number.percent): return math.floor(value(args[value.token]))
                else: return value
            except:
                return 0
        else:
            return value

def _values(tag, key, value=None):
    vars = Object.get(tag, '__variables__')
    if key[ : 6] == 'margin':
        return _margin(tag, vars, key, value)
    elif key[ : 10] == 'border-radius':
        return _corners(tag, vars, key, value)
    else:
        default, value = _get(tag.style, key, True)
        if default.type in ['append', 'complete', 'items', 'links']:
            values = ()
            for v in value: values += _value(tag, vars, *v),
            return values
        else:
             return _value(tag, vars, default, value)

def _parent(tag, key):
    if getVars(tag).isdoc:
        try: return tag.window.configure[key]
        except: pass
    else:
        (default, value), real = _get(tag.style, key, True), None
        if default != value: real = _values(tag, key)
        else: real = _parent(tag.parent, key)
        return real if real != None else default

# main
class new(Class.lock):
    __lock__ = ['click', 'current', 'default', 'focus', 'locked', 'hover', 'style']
    # attributes
    def __delattr__(self, key): _del(self, _realkey(key), 'style')
    def __getattr__(self, key): return _get(self, _realkey(key))
    def __setattr__(self, key, value): _set(self, _realkey(key), value, 'style')
    # item
    def __delitem__(self, key): _del(self, key, 'style')
    def __getitem__(self, key): return _get(self, key)
    def __setitem__(self, key, value): _set(self, key, value, 'style')
    # get
    def getDefault(self, key): return args.get(key)
    def getValue(self, key): return _values(self.tag, key)
    def getParent(self, key): return _parent(self.tag, key)
    # set
    def setClick(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'click')
    def setDefault(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'default')
    def setFocus(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'focus')
    def setHover(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'hover')
    def setLocked(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'locked')
    def setValue(self, key, value): return _values(self.tag, key, value)
    # main
    def __call__(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'style')
    def __init__(self, tag):
        # tag
        Object.set(self, 'tag', tag)
        Object.set(tag, 'style', self)
        # style
        Object.set(self, 'click', {})
        Object.set(self, 'current', {})
        Object.set(self, 'default', {})
        Object.set(self, 'focus', {})
        Object.set(self, 'hover', {})
        Object.set(self, 'locked', {})
        Object.set(self, 'style', {})
        Object.set(self, 'status', 'style')

class config(Class.lock):
    __lock__ = ['current', 'focus', 'locked', 'hover', 'style', 'window']
    # attributes
    def __delattr__(self, key): _del(self, _realkey(key), 'style')
    def __getattr__(self, key): return _get(self, _realkey(key))
    def __setattr__(self, key, value): _set(self, _realkey(key), value, 'style')
    # item
    def __delitem__(self, key): _del(self, key, 'style')
    def __getitem__(self, key): return _get(self, key)
    def __setitem__(self, key, value): _set(self, key, value, 'style')
    # get
    def getDefault(self, key): return config_args.get(key)
    # set
    def setFocus(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'focus')
    def setHover(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'hover')
    def setLocked(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'locked')
    # main
    def __call__(self, style=None, *argsv, **argsk): _setitems(self, style, argsk, 'style')
    def __init__(self, window):
        # window
        Object.set(window, 'configure', self)
        Object.set(self, 'window', window)
        # style
        Object.set(self, 'current', {})
        Object.set(self, 'focus', {})
        Object.set(self, 'hover', {})
        Object.set(self, 'locked', {})
        Object.set(self, 'style', {})
        Object.set(self, 'status', 'style')

def change(self, status):
    if status != 'lock':
        click = Object.get(self, 'click')
        current = Object.get(self, 'current')
        focus = Object.get(self, 'focus')
        hover = Object.get(self, 'hover')
        current.clear()
        if status == 'hover':
            current.update(hover)
        elif status == 'focus':
            current.update(focus)
        elif status == 'click':
            current.update(hover)
            current.update(click)
    Object.set(self, 'status', status)
