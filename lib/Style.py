########################################################
## Module  : Style         ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, os, re

# import local modules
from . import Array, Class, Number, String, Url

########################################################
## ------- here starts the module definitions ------- ##
########################################################

# color
class Color:
    __repr__ = Class.name('style', 'color')
    __str__ = __repr__

    # convert
    def rgba2hex(self):
        color = [0, 0, 0, 255]

        if type(self) in [list, tuple]:
            count = 0

            for item in self:
                try:
                    color[count] = int(item)
                    count += 1

                except:
                    break

        else:
            count = 1

            try:
                color[0] = int(self)

                for item in vals:
                    try:
                        color[count] = int(item)
                        count += 1

                    except:
                        break

            except:
                pass

        return '#%02x%02x%02x%02x' % tuple(color)

    def rgb2hex(self):
        return Color.rgba2hex(self)[0 : -2]

    def hex2rgba(self):
        color = self.lstrip('#')
        length = len(color)

        if length < 3:
            return 0, 0, 0, 0

        else:
            if length == 3:
                color = color * 2

            if length <= 6:
                color += 'ff'

            return tuple(int(color[i : i + 8 // 4], 16) for i in range(0, 8, 8 // 4))

    def hex2rgb(self):
        r, g, b, a = Color.hex2rgba(self)
        return r, g, b

    # mode
    def alpha(self, number):
        rgba = list(self.rgba)
        rgba[3] = number
        self.rgba = tuple(rgba)
        self.hexa = Color.rgba2str(self.rgba)

    def error(self):
        self.hex = '#000000'
        self.hexa = '#00000000'
        self.rgb = 0, 0, 0
        self.rgba = 0, 0, 0, 0

    def update(self, string):
        string = string.replace(' ', '')
        length = len(string)

        if string[0 : 1] == '#':
            if length in [4, 7, 9]:
                self.rgb = Color.hex2rgb(string)
                self.rgba = Color.hex2rgba(string)
                self.hex = Color.rgb2hex(self.rgb)
                self.hexa = Color.rgba2hex(self.rgba)

            else:
                self.error()

        else:
            try:
                open = string.find('(')
                close = string.find(')')
                rgba = string[0 if open == -1 else open : length if close == -1 else close].split(',')
                self.hex = Color.rgb2hex(rgba)
                self.hexa = Color.rgba2hex(rgba)
                self.rgb = Color.hex2rgb(self.hex)
                self.rgba = Color.hex2rgba(self.hexa)

            except:
                self.error()

    # start
    def __init__(self, string):
        self.update(string)

def Alpha(color, opacity=None):
    try:
        _float = float(opacity) * 100
        _round = round(2.55 * _float)
        color.alpha(255 if _round > 255 else _round)

    except:
        pass

    return color

def Mix(color1, color2, weight=None):
    string = '#'
    index = 1
    weight = weight if weight and type(weight) is int else 50

    for i in range(3):
        val1 = int(color1.hex[index : index + 2], 16)
        val2 = int(color2.hex[index : index + 2], 16)
        val3 = '%x' % math.floor(val2 + (val1 - val2) * (weight / 100.0))
        string += '0' + val3 if len(val3) <= 1 else val3
        index += 2

    color1.update(string)
    return color1

# number
inchType = 'pt'

def Calc(string, size=0, width=0, height=0):
    variables = {'%': size, 'w': width, 'h': height}
    return Number.inchCalc(string, inchType, variables)

def Percentage(string, size=0, width=0, height=0):
    variables = {'%': size, 'w': width, 'h': height}
    value, key, none = re.split('([^\d.]+)', string)
    return Number.inch((variables[key] / 100) * float(value), inchType)

# path
class Link(str):
    islink = Url.check
    openlink = Url.content

    def exists(self):
        return os.path.exists(self)

    def isdir(self):
        return os.path.isdir(self)

    def isfile(self):
        return os.path.isfile(self)

# events
class Event:
    callbacks = {
        'alpha': Alpha,
        'calc': Calc,
        'link': Link,
        'mix': Mix,
        'rgb': Color,
        'rgba': Color,
        'url': Link
    }

    def current(self, new=False):
        items = self.items
        keys = self.keys.copy()

        if len(keys) > 0:
            if not new:
                try: key = keys[-1]
                except: key = None

                try: del keys[-1]
                except: pass

            for k in keys:
                items = items[k]

        return items if new else (items, key)

    def add(self, value):
        items, key = self.current()
        items[key] += value

    def get(self):
        items, key = self.current()
        return items[key]

    def new(self):
        items = self.current(True)

        if type(items) is str:
            del self.keys[-1]
            items = self.current(True)

        count = len(items)
        items[count] = ''
        self.keys.append(count)

    def up(self):
        items, index = self.current()
        key = items[index]

        try: del items[index]
        except: pass

        try: del self.keys[-1]
        except: pass

        self.keys.append(key)
        items[key] = {}

        self.new()

    def value(string, *vals):
        devolve = string

        try:
            devolve = float(string)

        except:
            if re.search('(^\d+[%|w|h])$', string):
                devolve = Percentage(string, *vals)

            elif Number.isInch(string):
                devolve = Number.inch(string, inchType)

            elif string.lower() == 'false':
                devolve = False

            elif string.lower() == 'none':
                devolve = None

            elif string.lower() == 'true':
                devolve = True

            elif string[0 : 1] == '#':
                devolve = Color(string)

        return devolve

    def eval(self, start, *vals):
        try:
            devolve = []

            try:
                items = self.items.items()

            except:
                items = self.items()

            for k, v in items:
                if type(v) is dict:
                    value = None

                    try:
                        call = Event.callbacks[k]

                        if k == 'calc':
                            value = call(*tuple(Event.eval(v, False)) + vals)

                        else:
                            value = call(*tuple(Event.eval(v, False)))

                    except:
                        pass

                    devolve.append(value)

                else:
                    devolve.append(Event.value(v, *vals))

            if start and len(items) == 1:
                return devolve[0]

            else:
                return devolve

        except:
            return None

    def __init__(self, string):
        count = []
        on_space = True
        on_string = False

        self.keys = []
        self.items = {}
        self.new()

        for i in string:
            if i in ['"', "'"]:
                if on_string:
                    if on_string == i:
                        on_string = False

                    else:
                        self.add(i)

                elif self.get() == '':
                    on_string = i

                else:
                    self.add(i)

            elif not on_string and i == '(':
                if self.get() == '':
                    count.append(0)
                    self.add(i)

                else:
                    count.append(1)
                    self.up()

            elif not on_string and i == ')':
                if count[-1]:
                    try:
                        on_space = True
                        keys = list(reversed(self.keys))

                        for key in keys.copy():
                            del keys[0]

                            if type(key) is str:
                                break

                        self.keys = list(reversed(keys))

                    except:
                        pass

                else:
                    self.add(i)

                del count[-1]

            elif not on_string and i== ',':
                on_space = False
                self.new()

            elif not on_string and i == ' ':
                if on_space:
                    if len(self.keys) <= 1:
                        on_space = False
                        self.new()

                    else:
                        self.add(i)

            else:
                on_space = True
                self.add(i)

def Eval(string, *vals):
    if re.search('(.*?)\((.*?)\)', string):
        return Event(string).eval(True, *vals)

    else:
        try:
            devolve = []

            for value in string.split(' '):
                devolve.append(Event.value(value, *vals))

            if len(devolve) > 1:
                return devolve

            else:
                return devolve[0]

        except:
            return None

# items
class Item:
    def status(self, key):
        devolve = Array.copy(self.vars)

        try:
            devolve += self.data['status'][key]

        except:
            pass

        return devolve

    def attr(self, key):
        try:
            return Array.copy(self.data['attributes'][key])

        except:
            return Array.new()

    def __init__(self, data):
        self.data = data
        self.vars = data['variables']

class string:
    __repr__ = Class.name('style')
    __str__ = __repr__

    def get(self, key):
        data = self.data

        if Class.type(key) in ['array', 'list', 'tuple']:
            style = Array.new()
            style['variables'] = Array.new()
            style['status'] = Array.new()
            style['attributes'] = Array.new()

            try:
                if Class.type(key) == 'array':
                    keys = Array.keys(key)

                else:
                    keys = key

            except:
                keys = key

            for key in keys:
                values = data[key]

                if values:
                    style['variables'] += values['variables']
                    style['status'] += values['status']
                    style['attributes'] += values['attributes']
        else:
            try:
                style = data[key]

            except:
                style = Array.new()

        return Item(style)

    def decode(self, string):
        about = False
        close = False
        keys = None
        lines = string.split('\n')
        styles = {}

        for line in lines:
            _line = String.space(line)

            if _line != '' or _line[0 : 1] != '/':
                if _line[0 : 1] == '$':
                    try:
                        key, value = _line.split(':')
                        value = String.space(value)
                        self.vars[String.space(key)] = realValue(value)

                    except:
                        pass

                else:
                    start = line.find('{')
                    end = line.find('}')
                    _start = start + 1 if start != -1 else 0
                    _end = end if end != -1 else len(line)
                    _keys = line[0 : start if start != -1 else len(line)]
                    _line = line[_start : _end]

                    if start != -1:
                        close = True

                        if not keys:
                            keys = _keys.split(',')

                        elif len(_keys.replace(' ', '')) > 0:
                            keys += _keys.split(',')

                    elif keys and not close:
                        keys += _keys.split(',')

                    elif not close:
                        keys = _keys.split(',')

                    if close:
                        if len(_line) > 0:
                            for i in _line.split(';'):
                                try:
                                    key, value = i.split(':')
                                    value = String.swap(String.space(value), self.vars)
                                    styles[String.space(key)] = realValue(value)

                                except:
                                    pass

                        if end != -1:
                            for key in keys:
                                attr = None
                                key = String.space(key)

                                if key.find(':') != -1 or key.find('::') != -1:
                                    is_attr = key.find('::') != -1
                                    _find = key.find('::' if is_attr else ':')
                                    attr = key[_find + 2 if is_attr else _find + 1 : ]
                                    key = key[0 : _find]

                                if len(key) > 0:
                                    if key not in Array.keys(self.data):
                                        self.data[key] = Array.new()
                                        self.data[key]['variables'] = Array.new()

                                    if 'attributes' not in Array.keys(self.data[key]):
                                        self.data[key]['attributes'] = Array.new()

                                    if 'status' not in Array.keys(self.data[key]):
                                        self.data[key]['status'] = Array.new()

                                    if attr:
                                        if len(attr) > 0:
                                            if is_attr:
                                                if attr not in Array.keys(self.data[key]['attributes']):
                                                    self.data[key]['attributes'][attr] = Array.new()

                                                self.data[key]['attributes'][attr] += styles

                                            else:
                                                if attr not in Array.keys(self.data[key]['status']):
                                                    self.data[key]['status'][attr] = Array.new()

                                                self.data[key]['status'][attr] += styles
                                    else:
                                        self.data[key]['variables'] += styles

                            close = False
                            keys = None
                            styles = Array.new()

    def __init__(self, string):
        self.data = Array.new()
        self.string = ''
        self.vars = Array.new()

        if type(string) is str:
            self.string = string
            self.decode(string)
