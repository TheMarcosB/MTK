########################################################
## Module  : MTK.Tags      ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, tkinter, time

# import local modules
from . import Default, Event, Key, Style, Variables, Value, Text
from .Create import Body
from .Get import *
from .. import Class, Unique
from ..Main import *

# fixed variables
Titles = 0
Windows = []

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def createTk(self, title):
    global Titles
    data = getData(self)
    if Titles > 0: title = '%s-%s' % (title, Titles)
    if not Windows: tk = tkinter.Tk(className=title)
    else: tk = tkinter.Toplevel(Object.get(Windows[0], '__tk__'), {'class': title})
    Object.set(self, '__tk__', tk)
    x = round((tk.winfo_screenwidth() - 730) / 2)
    y = round((tk.winfo_screenheight() - 460) / 2)
    geometry = 730, 460, x, y
    icon = Variables.url(Paths.img + '/window/app.png').content.tkinter()
    data['geometry'] = geometry
    data['icon'] = icon
    tk.attributes('-type', 'splash')
    tk.tk.call('wm', 'iconphoto', tk, icon)
    tk.configure(bg='#cfcfcf')
    tk.geometry('%sx%s+%s+%s' % geometry)
    tk.title(title)
    if not Window.main and not Windows: Window.main = self
    Titles += 1
    Windows.append(self)

def Geometry(data, w, h, x, y):
    gw, gh, gx, gy = data['geometry']
    w = w if isinstance(w, int) else gw
    h = h if isinstance(h, int) else gh
    x = x if isinstance(x, int) else gx
    y = y if isinstance(y, int) else gy
    return w, h, x, y

def closePopup(event):
    if event.window != Window._popup and Window._popup != None:
        Window._popup.close()
        Window._popup = None

# bases
class Vars(dict):
    @property
    def size(self):
        if self.isdoc:
            return self.getsize
        else:
            w, h = self.padsize
            bt, br, bb, bl = self.tag.style.borderWidth
            w += br + bl
            h += bt + bb
            return w, h

    @property
    def w(self): return self.size[0]
    @property
    def h(self): return self.size[1]

    @property
    def padsize(self):
        if self.isdoc:
            return self.getsize
        else:
            w, h = self.getsize
            pt, pr, pb, pl = self.tag.style.padding
            w += pr + pl
            h += pt + pb
            return w, h

    @property
    def getsize(self):
        if self.isdoc:
            pd = (self.tag.window.configure.padding + self.tag.window.configure.borderWidth) * 2
            w, h = self.tag.window.size
            return w - pd, h - pd
        else:
            return self.insize

    @property
    def bx(self): return self.x + (0 if self.isdoc else self.tag.style.borderWidth[3])
    @property
    def by(self): return self.y + (0 if self.isdoc else self.tag.style.borderWidth[0])
    @property
    def px(self): return self.bx + (0 if self.isdoc else self.tag.style.padding[3])
    @property
    def py(self): return self.by + (0 if self.isdoc else self.tag.style.padding[0])

    def clear(self):
        self.end, self.length, self.left, self.right, self.top, self.width = 0, 0, 0, 0, 0, 0

    def __init__(self, tag, tk=None, parent=None):
        self.tag, self.parent = tag, getVars(parent) if parent else parent
        self.font, self.value = None, None
        self.expand, self.insize = None, (0, 0)
        self.position, self.x, self.y = (None, None), 0, 0
        self.moveX, self.moveY = 0, 0
        self.scrollX, self.scrollY = 0, 0
        self.isdoc, self.isover = isinstance(self.tag, Document), False
        self.display, self.istk = None, tk
        self.name = None
        if self.isdoc:
            self.document, self.window = tag, tag.window
        else:
            canvas = self.istk if self.istk else self.parent.canvas
            self.canvas, self.document, self.window = canvas, self.parent.document, self.parent.window
            self.check = {
                'shadow-outset': {},
                'frame': {},
                'background': {},
                'shadow-inset': {}
            }
            if isinstance(canvas, tkinter.Canvas):
                self.update({
                    'shadow-outset': canvas.create_image((0, 0), anchor='nw', state='hidden'),
                    'frame': canvas.create_image((0, 0), anchor='nw', state='hidden'),
                    'background': canvas.create_image((0, 0), anchor='nw', state='hidden'),
                    'shadow-inset': canvas.create_image((0, 0), anchor='nw', state='hidden')
                })
                if isinstance(tag, Photo):
                    self.check['image'] = {}
                    self['image'] = canvas.create_image((0, 0), anchor='nw', state='hidden')
                elif isinstance(tag, Label):
                    self.check.update({
                        'text-shadow': {},
                        'text': {}
                    })
                    self.update({
                        'text-shadow': canvas.create_image((0, 0), anchor='nw', state='hidden'),
                        'text': canvas.create_image((0, 0), anchor='nw', state='hidden')
                    })
        self.clear()
        Object.set(tag, '__variables__', self)

class Base(Class.lock):
    __allow__ = ['className', 'id', 'name']
    @property
    def realTag(self): return self.__class__.__name__.lower()
    @property
    def className(self): return self.getAttr('class')
    @property
    def className(self, value): self.setAttr('class', value)
    @property
    def id(self): return self.getAttr('id')
    @property
    def id(self, value): self.setAttr('id', value)
    @property
    def name(self): return self.getAttr('name')
    @property
    def name(self, value): self.setAttr('name', value)
    @property
    def parents(self):
        devolve = []
        while True:
            devolve.append(self)
            if isinstance(self, Document): break
            elif self.parent: self = self.parent
        return list(reversed(devolve))

    # string
    def __repr__(self):
        return '<Element%s>' % self.tagName.capitalize()

    def __str__(self):
        return self.__repr__()

    # main
    def delete(self, parent=False):
        vars = getVars(self)
        for tag in vars.values(): vars.canvas.delete(tag)
        if not parent:
            self.parent.items.delete(self)
            parent = True
        if isinstance(self, Frame):
            for item in self.items: item.delete(parent)

    def __init__(self, name, tk, parent):
        Vars(self, tk, parent)
        Object.set(self, '__data__', {})
        Object.set(self, '__id__', Unique.id())
        Object.set(self, '__tk__', tk)
        Object.set(self, 'parent', parent)
        Object.set(self, 'tagName', name.lower())
        Event.Attr(self)
        Style.new(self)
        Event.On(self)
        Event.Add(self)
        Value.set(self)
        if isinstance(self, (Label, Edit)):
            Text.new(self)

class Items(list):
    # items
    def __find__(self, key, tag):
        if type in ['id', 'name']: devolve = None
        else: devolve = Items()
        for item in reversed(self):
            try:
                if tag == 'tag' and key == item.tagName: list.append(devolve, item)
                elif tag == 'id' and key == item.getAttr('id'): devolve = item
                elif tag == 'class':
                    names, count = item.getAttr('name'), 0
                    for name in names:
                        if name + ' ' in key + ' ': count += 1
                    if count == len(names): list.append(devolve, item)
                elif tag == 'name' and key == item.getAttr('name'): devolve = item
                elif tag == 'type' and key == item.getAttr('type'): list.append(devolve, item)
            except:
                pass
            if isinstance(item.items, Items) and len(item.items) > 0:
                if tag in ['id', 'name']: devolve = item.items.__find__(key, tag)
                else: devolve += item.items.__find__(key, tag)
        return devolve

    def getItems(self):
        devolve = Items()
        for item in self:
            devolve.append(item)
            if isinstance(item, Frame): devolve += item.getItems()
        return devolve

    def getByClass(self, key):
        return self.__find__(key, 'class')

    def getById(self, key):
        return self.__find__(key, 'id')

    def getByName(self, key):
        return self.__find__(key, 'name')

    def getByTag(self, key):
        return self.__find__(key, 'tag')

    # index
    def index(self, widget):
        if isinstance(widget, Base):
            index = 0
            for item in self:
                if widget.__id__ == item.__id__:
                    return index
                index += 1
        return -1

    def __delitem__(self, *argsv):
        pass

    def __getitem__(self, index):
        try: return list.__getitem__(self, index)
        except: pass

    def __setitem__(self, *argsv):
        pass

    # widget
    def append(self, widget):
        if isinstance(widget, Base):
            list.append(self, widget)

    def delete(self, widget):
        if isinstance(widget, Base):
            index = list.index(self, widget)
            list.__delitem__(self, index)

    def __init__(self, tag=None):
        if tag:
            Object.set(tag, 'items', self)
            Object.set(tag, 'getItems', self.getItems)
            Object.set(tag, 'getByClass', self.getByClass)
            Object.set(tag, 'getById', self.getById)
            Object.set(tag, 'getByName', self.getByName)
            Object.set(tag, 'getByTag', self.getByTag)
            Object.set(tag, 'getIndex', self.index)

# widgets
class Photo(Base):
    __allow__ = Base.__allow__ + ['src']

    @property
    def src(self):
        return self.getAttr('src', '')

    @src.setter
    def src(self, value):
        img = Variables.src(value)
        if img: self.style['-image'] = img
        self.setAttr('src', value)

class Icon(Photo):
    __allow__ = Photo.__allow__ + ['icon']

    @property
    def icon(self): return self.getAttr('icon', '')

    @icon.setter
    def icon(self, value):
        self.src = '%s/icons/%s.png' % (Paths.img, value)
        self.setAttr('icon', value)

class Status(Photo):
    __allow__ = Photo.__allow__ + ['status', 'value']
    @property
    def status(self): return self.getAttr('status', 0)
    @status.setter
    def status(self, value): self.setAttr('status', value)
    @property
    def value(self): return self.getAttr('value', 0)
    @value.setter
    def value(self, value): self.setAttr('value', value)

class Label(Base):
    __allow__ = Base.__allow__ + ['value']
    @property
    def value(self): return self.getAttr('value', '')
    @value.setter
    def value(self, value): self.setAttr('value', value)
    def __len__(self): return len(self.value)

class Edit(Label):
    def addValue(self, value):
        text = getTx(self)
        text.event, text.key = 'paste', str(value)
        bar = text.bar
        if not bar: text.bar = self.style.getValue('size')
        Key.edit(self)

    def delValue(self):
        text = getTx(self)
        text.event, text.key = 'delete', ''
        bar = text.bar
        if not bar: text.bar = 0, 0
        Key.edit(self)

    def backscape(self):
        text = getTx(self)
        text.event, text.key = 'backscape', ''
        bar = text.bar
        if not bar: text.bar = self.style.getValue('size')
        Key.edit(self)

class Item(Label):
    __allow__ = Label.__allow__ + ['selected']
    @property
    def selected(self): return self.getAttr('selected', 'off')
    @selected.setter
    def selected(self, value): self.setAttr('selected', value)

class Select(Label):
    def createItem(self, *argsv):
        items = []
        for value in argsv:
            widget = Item('item', None, self)
            widget.value = value
            self.items.append(widget)
            items.append(widget)
        return items[0] if len(items) == 1 else items

    def __init__(self, *argsv):
        Label.__init__(self, *argsv)
        Items(self)

class Frame(Base):
    def createTag(self, value, type=None):
        tags = {'icon': Icon, 'image': Photo, 'label': Label, 'frame': Frame}
        if isinstance(value, tuple): name, tk = value[0].lower(), value[1]
        else: name, tk = value.lower(), None
        if type and tags.get(type):
            widget = tags[type](name, None, self)
        else:
            if name in ['check', 'radio', 'switch']: widget = Status(name, tk, self)
            elif name in ['img', 'image', 'photo']: widget = Photo(name, tk, self)
            elif name in ['button', 'label', 'title']: widget = Label(name, tk, self)
            elif name in ['entry', 'text']: widget = Edit(name, tk, self)
            elif name in ['line', 'separator']: widget = Base(name, tk, self)
            elif name == 'icon': widget = Icon(name, tk, self)
            elif name == 'link': widget = Link(name, tk, self)
            elif name == 'select': widget = Select(name, tk, self)
            else: widget = Frame(name, tk, self)
        self.items.append(widget)
        return widget

    def __init__(self, *args):
        Base.__init__(self, *args)
        Items(self)

# window
class Document(Class.lock):
    createTag = Frame.createTag

    def __init__(self, window, type):
        Object.set(self, 'window', window)
        Object.set(window, 'document', self)
        Object.set(self, '__tk__', getTk(window))
        Items(self)
        Vars(self)
        Body.create(self, type)

class Window(Class.lock):
    __allow__ = [
        'size', 'width', 'height',
        'position', 'x', 'y',
        'resizable', 'widthresizable', 'heightresizable',
        'title'
    ]
    main = None
    _popup = None

    # configure
    def geometry(self, width=None, height=None, x=None, y=None):
        data = getData(self)
        if (width, height, x, y) != (None, ) * 4:
            if data['status'] != 'fullscreen':
                geometry = Geometry(data, width, height, x, y)
                if data['geometry'] != geometry:
                    tk, geo, data['geometry'] = getTk(self), data['geometry'], geometry
                    tk.geometry('%dx%d+%d+%d' % getGeo(geometry))
                    if getStatus(self) in ['left', 'maximize', 'right']:
                        tk.update()
                        data['geometry'] = tk.winfo_width(), tk.winfo_height(), tk.winfo_x(), tk.winfo_y()
                    Body.resize(self)
                    if geo[ : 2] != geometry[ : 2]: Event.Exec(self, 'resize')
                    if geo[2: ] != geometry[2 : ]: Event.Exec(self, 'reposition')
        else:
            return data['geometry']

    def resize(self, width=None, height=None, x=None, y=None, geometry=None):
        data = getData(self)
        if (width, height, x, y) != (None, ) * 4:
            data['resize'] = data['geometry']
            self.geometry(*Geometry(data, width, height, x, y))
        else:
            self.geometry(*(geometry if geometry else data['resize']))
            data['resize'] = None

    @property
    def title(self):
        return getTk(self).title()

    @title.setter
    def title(self, value):
        title = str(value)
        getTk(self).title(title)

    # time
    def setTimeout(self, function, timer, args=None, stop=None):
        Object.get(self, '__timeout__').append(Event.Time(self, function, timer, args, stop, 'timeout'))

    def setInterval(self, function, timer, args=None, stop=None):
        Object.get(self, '__interval__').append(Event.Time(self, function, timer, args, stop, 'interval'))

    def setLoop(self, function, args=None, stop=None):
        Object.get(self, '__loop__').append(Event.Time(self, function, None, args, stop, 'loop'))

    # size
    @property
    def width(self): return self.geometry()[0]
    @width.setter
    def width(self, value): self.geometry(width=value)
    @property
    def height(self): return self.geometry()[1]
    @height.setter
    def height(self, value): self.geometry(height=value)
    @property
    def size(self): return self.geometry()[ : 2]
    @size.setter
    def size(self, value): self.geometry(width=value[0], height=value[1])

    # screen
    @property
    def screenwidth(self): return getTk(self).winfo_screenwidth()
    @property
    def screenheight(self): return getTk(self).winfo_screenheight()
    @property
    def screensize(self): return self.screenwidth, self.screenheight

    # resizable
    @property
    def resizable(self): return getData(self)['resizable']
    @resizable.setter
    def resizable(self, value): getData(self)['resizable'] = value
    @property
    def widthresizable(self): return self.resizable[0]
    @widthresizable.setter
    def widthresizable(self, value): self.resizable = value, self.heightresizable
    @property
    def heightresizable(self): return self.resizable[1]
    @heightresizable.setter
    def heightresizable(self, value): self.resizable = self.widthresizable, value

    # position
    @property
    def x(self): return self.geometry()[2]
    @x.setter
    def x(self, value): self.geometry(x=value)
    @property
    def y(self): return self.geometry()[3]
    @y.setter
    def y(self, value): self.geometry(y=value)
    @property
    def position(self): return self.geometry()[2 : ]
    @position.setter
    def position(self, value): self.geometry(x=value[0], y=value[1])

    # maximize
    @property
    def maxsize(self): return getTk(self).maxsize()
    @property
    def maxwidth(self): return self.maxsize[0]
    @property
    def maxheight(self): return self.maxsize[1]
    @property
    def maxx(self): return math.floor(self.screenwidth - self.maxwidth)
    @property
    def maxy(self): return math.floor(self.screenheight - self.maxheight)
    @property
    def maxposition(self): return self.maxx, self.maxy
    @property
    def maxgeo(self): return self.maxsize + self.maxposition

    # pointer
    @property
    def pointerx(self): return getTk(self).winfo_pointerx()
    @property
    def pointery(self): return getTk(self).winfo_pointery()
    @property
    def pointer(self): return self.pointerx, self.pointery

    # window
    def close(self, *argsv, **argsk):
        Event.Exec(self, 'close')
        index = Windows.index(self)
        del Windows[index]
        if index == 0: Window.main = None
        if Window._popup == self: Window._popup = None
        getTk(self).destroy()

    def fullscreen(self, *argsv, **argsk):
        data, tk = getData(self), getTk(self)
        if data['status'] == 'fullscreen':
            setStatus(self)
            geometry, fullscreen = data['geometry'], data['fullscreen']
            data['geometry'] = data['fullscreen']
            tk.attributes('-fullscreen', False)
            tk.attributes('-type', 'splash')
        else:
            setStatus(self, 'fullscreen')
            geometry = data['fullscreen'] = data['geometry']
            fullscreen = data['geometry'] = self.screensize + (0, 0)
            tk.attributes('-type', 'normal')
            tk.attributes('-fullscreen', True)
        if not argsk.get('_no_resize'):
            if geometry[ : 2] != fullscreen[ : 2]:
                Event.Exec(self, 'resize')
            if geometry[2 : ] != fullscreen[2 : ]:
                Event.Exec(self, 'reposition')
        Event.Exec(self, 'fullscreen')

    def maximize(self, *argsv, **argsk):
        status = getStatus(self)
        if status == 'fullscreen':
            self.fullscreen(_no_resize=True)
        if status != 'maximize':
            setStatus(self, 'maximize')
            self.resize(*(self.screensize + (0, 0)))
        else:
            setStatus(self, 'normal')
            self.resize(**argsk)
        Event.Exec(self, 'maximize')

    def minimize(self, *argsv, **argsk):
        setStatus(self, 'minimize')
        Event.Exec(self, 'minimize')
        getTk(self).iconify()

    # main
    def popup(self, w, h, x, y):
        if Window._popup != None: Window._popup.close()
        popup = Window(type='popup')
        popup.geometry(w, h, x, y)
        Window._popup = popup
        return popup

    def __init__(self, title='TheMarcosBC.MTK', type='normal'):
        Object.set(self, '__id__', Unique.id())
        Object.set(self, '__loop__', [])
        Object.set(self, '__interval__', [])
        Object.set(self, '__timeout__',[])
        Object.set(self, '__data__', {
            'type': type,
            'status': 'normal',
            'resizable': (True, True),
            'resize': None
        })
        createTk(self, title)
        Event.Bind(self)
        Event.On(self)
        Event.Add(self)
        Style.config(self)
        Document(self, type)
        Event.New(self)
        self.addEvent('click', closePopup)
        self.addEvent('click', Default.window_click)
        self.addEvent('press', Default.window_press)
        self.addEvent('move', Default.window_resize)
