#########################################################
## Module  : MTK.Event      ## Author   : Marcos Bento ##
## ------------------------ ## ----------------------- ##
## Github  : TheMarcosBC    ## Twitter  : TheMarcosBC  ##
## ------------------------ ## ----------------------- ##
## Facebook: TheMarcosBC    ## Instagram: TheMarcosBC  ##
#########################################################

# import default modules
import collections, math, time

# import local modules
from . import Default, Key, Style
from .Create import Select
from .Get import *
from .. import Class
from ..Main import *

# fixed variables
Globals = {}

#########################################################
## -------- here starts the module definitions ------- ##
#########################################################
class Attr(Class.lock):
    __lock__ = ['__attrs__', '__on__']

    def append(self, name, value):
        before = Object.get(self, '__attrs__').get(name)
        callback =  Object.get(self, '__on__').get(name)
        if value != before and callback: value = callback(self.tag, value)
        Object.get(self, '__attrs__')[name] = value

    def delete(self, name):
        try: del Object.get(self, '__attrs__')[name]
        except: return False
        return True

    def __call__(self, name, default=None):
        return Object.get(self, '__attrs__').get(name, default)

    def __init__(self, tag):
        Object.set(self, '__attrs__', {})
        Object.set(self, '__on__', {})
        Object.set(self, 'tag', tag)
        Object.set(tag, 'getAttr', self)
        Object.set(tag, 'delAttr', self.delete)
        Object.set(tag, 'setAttr', self.append)
        if tag.tagName in ['check', 'radio', 'switch']:
            AttrEvent(self, 'value', Default.status_value)

class Add(Class.lock):
    def delete(self, function):
        events, key = Object.dict(self), None
        for event, list in events.items():
            index = 0
            for i in list:
                if i == function:
                    key = event
                    break
                index += 1
        if key and index: del events[key][index]

    def __call__(self, event, function):
        if not Object.get(self, event): Object.set(self, event, [])
        list = Object.get(self, event)
        list.append(function)

    def __init__(self, widget):
        Object.set(widget, 'addEvent', self)
        Object.set(widget, 'delEvent', self.delete)
        if widget.tagName in ['check', 'radio', 'switch']:
            self('click', Default.status_event)
        elif widget.tagName == 'select':
            self('click', Select.create)
        elif widget.tagName in ['entry', 'text']:
            self('press', Key.eventpress)
            self('click', Key.eventclick)
            self('keypress', Key.eventkey)

class New(Class.lock):
    focused = None
    hovered = None
    # screen
    def screen_width(self): return self.window.screenwidth
    @property
    def screen_height(self): return self.window.screenheight
    @property
    def screen_x(self): return self.window.pointerx
    @property
    def screen_y(self): return self.window.pointery
    # window
    @property
    def width(self): return self.window.width
    @property
    def height(self): return self.window.height
    @property
    def x(self): return self.screen_x - self.window.x
    @property
    def y(self): return self.screen_y - self.window.y

    def __init__(self, window):
        Object.set(self, 'window', window)
        Object.set(self, 'document', window.document)
        Object.set(self, 'setLoop', window.setLoop)
        Object.set(self, 'setInterval', window.setInterval)
        Object.set(self, 'setTimeout', window.setTimeout)
        Object.set(window, 'event', self)

class On(Class.lock):
    __lock__ = ['__on__', '__tag__']

    def __delattr__(self, key):
        try: del Object.get(self, '__on__')[key]
        except: pass

    def __getattr__(self, key):
        return Object.get(self, '__on__').get(key)

    def __setattr__(self, key, value):
        Object.get(self, '__on__')[key] = value

    def __getitem__(self, key):
        return Object.get(self, '__on__').get(key)

    def __call__(self, key, value):
        self.__setattr__(key, value)

    def __init__(self, widget):
        Object.set(self, '__on__', {})
        Object.set(widget, 'on', self)

class Time(Class.lock):
    __lock__ = ['add', 'args', 'function', 'end', 'start']

    @property
    def timer(self):
        return round((Object.get(self, 'end') - Object.get(self, 'start')) * 1000)

    @property
    def count(self):
        return round(self.timer() / 1000)

    def stop(self):
        type, window = Object.get(self, 'type'), Object.get(self, 'window')
        try:
            if type == 'timeout': parent = Object.get(window, '__timeout__')
            elif type == 'interval': parent = Object.get(window, '__interval__')
            else: parent = Object.get(window, '__loop__')
            index = parent.index(self)
            del parent[index]
        except:
            pass

    def __init__(self, window, function, timer, args, stop, type):
        if isinstance(stop, Time): stop.stop()
        Object.set(self, 'args', args)
        Object.set(self, 'window', window)
        Object.set(self, 'document', window.document)
        Object.set(self, 'function', function)
        Object.set(self, 'type', type)
        if type != 'loop':
            start, add = time.time(), timer / 1000
            Object.set(self, 'start', start)
            Object.set(self, 'add', add)
            Object.set(self, 'end', start + add)

def Timer(self):
    function = Object.get(self, 'function')
    args, type = Object.get(self, 'args'), Object.get(self, 'type')
    add, end = Object.get(self, 'add'), Object.get(self, 'end')
    try:
        if type == 'loop':
            if isinstance(args, (list, tuple)): function(*args)
            else: function(self)
        else:
            timer = time.time()
            if timer >= end:
                if type == 'interval':
                    if isinstance(args, (list, tuple)): function(*args)
                    else: function(self)
                    Object.dict(self)['end'] += add
                else:
                    if isinstance(args, (list, tuple)): function(*args)
                    else: function(self)
                    self.stop()
    except Exception as e:
        print(e)
        self.stop()

def Execute(event, function):
    if function and isinstance(function, collections.Callable):
        function(event)
    elif function and isinstance(function, str):
        try:
            Globals.update({
                'document': event.document,
                'event': event,
                'widget': event.widget,
                'window': event.window
            })
            exec(function, Globals, Globals)
        except:
            pass

def Events(event, widget, type):
    # events
    events = Object.dict(widget.addEvent).get(type)
    if events:
        for function in events:
            Execute(event, function)
    # on
    function = widget.on[type]
    if not function and widget.getAttr:
        function = widget.getAttr('on' + type.title())
    Execute(event, function)

def CommandTag(event, tag, type, isrelative=False):
    if not getData(event.window).get('headerbar-move'):
        vars = getVars(tag)
        width, height = vars.padsize
        event.x = max(min(math.floor(event.window_x - (vars.bx + 5)), width), 0)
        event.y = max(min(math.floor(event.window_y - (vars.by + 5)), height), 0)
        event.widget = tag
        if type == 'move' and not vars.isover:
            vars.isover = True
            Style.change(tag.style, 'hover')
            CommandTag(event, tag, 'over')
        elif type == 'out':
            vars.isover = False
            Style.change(tag.style, 'style')
        Events(event, tag, type)
        isparent = not vars.parent.isdoc and not type in ['out', 'over']
        isrelative = type == 'move' or tag.style['relative'] == 'on' or isrelative
        if isparent and isrelative: CommandTag(event, tag.parent, type, True)

def Command(event, window, type):
    if not type in ['over', 'out'] or (event.widget == '.' or event.widget == getTk(window)):
        try:
            event.x, event.y = event.window_x, event.window_y
        except:
            event.window, event.document = window, window.document
            try:
                tk, (gw, gh) = getTk(window), window.size
                event.screen_x, event.screen_y = event.x_root, event.y_root
                event.x, event.y = event.x_root - tk.winfo_x(), event.y_root - tk.winfo_y()
                if getStatus(window) == 'normal':
                    event.x += gw - tk.winfo_width()
                    event.y += gh - tk.winfo_height()
                del event.x_root
                del event.y_root
            except:
                pass
            event.window_x, event.window_y = event.x, event.y
        event.type, event.widget = type, None
        Events(event, window, type)
        pd = window.configure.padding + window.configure.borderWidth
        if not type in ['cursor', 'over'] and event.x > pd and event.y > pd:
            iswidget, x, y = False , max(event.x - pd, 0),  max(event.y - pd, 0)
            doc = window.document
            if getData(window)['type'] == 'normal':
                buttons, header, body = doc.buttons, doc.headerbar, doc.body
                buttonsItems = tuple(reversed(buttons.getItems())) + (buttons, )
                headerItems = tuple(reversed(header.getItems())) + (header, )
                bodyItems = tuple(reversed(body.getItems())) + (body, )
                items = buttonsItems + headerItems + bodyItems
            else:
                items = reversed(doc.getItems())
            for tag in items:
                vars = getVars(tag)
                if type != 'out':
                    ix = x >= vars.x and x <= vars.x + vars.w
                    iy = y >= vars.y and y <= vars.y + vars.h
                    if ix and iy:
                        if not iswidget:
                            iswidget = True
                            CommandTag(event, tag, type)
                    elif vars.isover:
                        CommandTag(event, tag, 'out')
                elif vars.isover and type == 'out':
                    CommandTag(event, tag, 'out')

def Exec(window, name):
    function = window.on[name]
    if isinstance(function, collections.Callable):
        try:
            function(window)
        except:
            try: function()
            except: pass

class EventKey:
    def clear(self):
        self.event = self.down = None
        self.time = self.timePress = None
        self.isPress = False

    def loop(self, event):
        if self.time != None:
            if time.time() - self.time <= 0.01:
                if not self.timePress or time.time() - self.timePress > 0.02:
                    Command(self.event, self.window, 'keypress')
                    self.timePress = time.time()
                getData(self.window)['update-time'] = time.time()
            elif time.time() - self.time >= 0.5:
                Command(self.event, self.window, 'keyup')
                self.clear()

    def press(self, event):
        self.isPress = True
        if not self.down or self.down.keysym != event.keysym:
            Command(event, self.window, 'keydown')
            self.down = event
        self.event = event
        self.time = time.time()

    def __init__(self, window):
        self.window = window
        self.clear()
        Object.set(window, '__key__', self)
        window.setLoop(self.loop)

def Bind(window):
    tk = getTk(window)
    tk.bind('<Button-1>', lambda event: Command(event, window, 'press'))
    tk.bind('<ButtonRelease-1>', lambda event: Command(event, window, 'click'))
    # key
    key = EventKey(window)
    tk.bind('<Key>', key.press)
     # mouse
    tk.bind('<Motion>', lambda event: Command(event, window, 'move'))
    tk.bind('<Enter>', lambda event: Command(event, window, 'over'))
    tk.bind('<Leave>', lambda event: Command(event, window, 'out'))
    # wheel
    tk.bind('<Button-4>', lambda event: Command(event, window, 'wheelup'))
    tk.bind('<Button-5>', lambda event: Command(event, window, 'wheeldown'))
