########################################################
## Module  : Number        ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, re

# import local modules
from . import Array, Error
from .Main import *

# fixed variables
_bytetypes = {
    1000: [
        ['kb',  'kilo'],
        ['mb',  'mega'],
        ['gb',  'giga'],
        ['tb',  'tera'],
        ['pb',  'peta'],
        ['eb',  'exa'],
        ['zb',  'zetta'],
        ['yb',  'yotta']
    ],

    1024: [
        ['kib',  'kibi'],
        ['mib',  'mebi'],
        ['gib',  'gibi'],
        ['tib',  'tebi'],
        ['pib',  'pebi'],
        ['eib',  'exbi'],
        ['zib',  'zebi'],
        ['yib',  'yobi']
    ]
}
_inchtypes = {
    'cm': 2.54,
    'chx': 12,
    'chy': 6,
    'en': 144.54,
    'em': 6,
    'ex': 13.1,
    'in': 1,
    'm': 0.0254,
    'mm': 25.4,
    'pc': 6,
    'pcp': 6.02250006,
    'pt': 72,
    'ptp': 72.27,
    'px': 96,
    'tw': 1440
}

########################################################
## ------- here starts the module definitions ------- ##
########################################################
class percent(float):
    def floor(self):
        return math.floor(self.real)

    def int(self):
        return round(self.real)

    def __call__(self, value):
        return (value / 100) * self.real

    def __new__(cls, value, token='%', *argsv, **argsk):
        if isinstance(value, str):
            value, _token, *args = re.split('([^-\d.]+)', value)
            if _token == token or _token in token:
                try: value = float(value)
                except: value = 0
            else:
                _token = '%'
                value = 0
            self = float.__new__(cls, value, *argsv, **argsk)
            self.token = _token
            return self

# inch
def _inchsplit(value, new_token):
    value, token, *args = re.split('([^-\d.]+)', value)
    return (float(value) / _inchtypes[token]) * _inchtypes[new_token]

def _inchvalue(value, token):
    devolve = 0
    if isinstance(value, (float, int)):
        devolve = value
    else:
        try: _inchsplit(value, token)
        except: pass
    return devolve

class inch(float):
    # convert
    def __getitem__(self, token):
        if isinstance(token, str):
            try: return inch((self.real / _inchtypes[self.token]) * _inchtypes[token.lower()], token)
            except: return self
        else:
            return self

    def __getattr__(self, key):
        if key in _inchtypes.keys(): return self[key]
        else: return object.__getattr__(self, key)

    def floor(self, token=None):
        return math.floor(self[token].real)

    def int(self, token=None):
        return round(self[token].real)

    # add calculation
    def __iadd__(self, value):
        return inch(self.real + _inchvalue(value, self.token), self.token)

    def __isub__(self, value):
        return inch(self.real - _inchvalue(value, self.token), self.token)

    def __imul__(self, value):
        return inch(self.real * _inchvalue(value, self.token), self.token)

    def __itruediv__(self, value):
        return inch(self.real / _inchvalue(value, self.token), self.token)

    # send calculation
    __add__ = __iadd__
    __sub__ = __isub__
    __mul__ = __imul__
    __truediv__ = __itruediv__

    # main
    def __str__(self):
        return format(self.real, '.4g') + self.token

    def __repr__(self):
        return repr(self.__str__())

    def __new__(cls, value=0, token='in', *argsv, **argsk):
        strtoken, strvalue = None, None
        if isinstance(value, str):
            try:
                items = re.split('([^-\d.]+)', value.replace(' ', ''))
                if len(items) > 1:
                    strvalue, strtoken, *args = items
                    strvalue = float(strvalue)
                else:
                    value = float(value)
            except:
                value = 0
        try:
            token = token.lower()
            multi = _inchtypes[token]
            if strtoken: value = (strvalue / _inchtypes[strtoken.lower()]) * multi
        except:
            token, value = 'in', 0
        try: self = float.__new__(cls, value, *argsv, **argsk)
        except: self = float.__new__(cls, 0, *argsv, **argsk)
        self.token = token
        return self

class inchcalc(inch):
    def __eq__(self, other):
        return isinstance(other, inchcalc) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def _calc(value, token='in', *argsv, **argsk):
        devolve, error = 0, None
        if isinstance(value, str):
            script = value.replace(' ', '')
            if Array.iskeys(getItem(argsv, 0)): argsk.update(Array.todict(argsv[0]))
            for item in re.findall('([-]?\d+[\w|%]+)', script):
                try:
                    value, key, *args = re.split('([^-\d.]+)', item)
                    if key in argsk.keys(): value = (argsk[key] / 100) *  float(value)
                    else: value = _inchsplit(item, token)
                    script = script.replace(item, str(value))
                except:
                    error = "set default value of '%s' for calculation" % item
                    script = script.replace(item, '0')
            try: devolve += eval(script)
            except: error = "invalid value '%s' does not calculate" % item
        elif isinstance(value, (float, int)) and value > 0:
            devolve += value
        return devolve, error

    def __call__(self, *argsv, **argsk):
        value, error = inchcalc._calc(self.value, self.token, *argsv, **argsk)
        self = inch(value, self.token)
        if error: Error.set(self, Error.new('inchcalc', error))
        return self

    def __new__(cls, value=0, token='in', iserror=True, *argsv, **argsk):
        val, error = inchcalc._calc(value, token, *argsv, **argsk)
        self = inch.__new__(cls, val, token)
        self.value = value
        if error and iserror: Error.set(self, Error.new('inchcalc', error))
        return self

# byte
def _bytetoken(token):
    devolve, token = (8, 'byte'), token.lower()
    if token[-1 : ] == 's': token = token[0 : -1]
    if token.find('byte') >= 4: token = token[0 : token.find('byte')]
    if token == 'bit': devolve = 1, 'bit'
    elif not token in ['b', 'byte']:
        for number, values in _bytetypes.items():
            count = 1
            for keys in values:
                if token in keys:
                    devolve = 8 * (number ** count), keys[0]
                    break
                count += 1
    return devolve

def _tobyte(value):
    devolve = 0
    if isinstance(value, float):
        try: devolve = (value.real * value.multi) / 8
        except: devolve = value
    elif isinstance(value, int):
        devolve = value
    else:
        try:
            value, token = re.findall('(\d+)([^\d]+)', value)[0]
            devolve = (float(value) * _bytetoken(token)[0]) / 8
        except:
            pass
    return devolve

class byte(float):
    # convert
    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                multi, token = _bytetoken(key)
                return byte((self.real * self.multi) / multi, token)
            except:
                return self
        else:
            return self

    def floor(self, token=None):
        return math.floor(self[token].real)

    def int(self, token=None):
        return round(self[token].real)

    # add calculation
    def __iadd__(self, value):
        return byte(_tobyte(self) + _tobyte(value))

    def __isub__(self, value):
        return byte(_tobyte(self) - _tobyte(value))

    def __imul__(self, value):
        return byte(self.real * _tobyte(value))

    def __itruediv__(self, value):
        return byte((_tobyte(self) / _tobyte(value)) * (self.multi / 8))

    # send calculation
    __add__ = __iadd__
    __sub__ = __isub__
    __mul__ = __imul__
    __truediv__ = __itruediv__

    # main
    def __str__(self):
        if self.token in ['bit', 'byte']:
            devolve = '%s %s' % (int(self.real), self.token.capitalize())
            if self.real > 1: devolve += 's'
        else:
            devolve = format(self.real, '.1f')
            if devolve[-2 : ] == '.0': devolve = devolve[ : -2]
            devolve += ' ' + self.token.upper()
        return devolve

    def __repr__(self):
        return repr(self.__str__())

    def __new__(cls, value=0, token=None, *argsv, **argsk):
        if isinstance(value, str):
            try:
                items = re.split('([^\d.]+)', value.replace(' ', ''))
                if len(items) > 1:
                    value, token, *args = items
                    value = float(value)
                else:
                    value = float(value)
            except:
                pass
        if token == None:
            if value > 0:
                index = math.floor(math.log(value, 1000))
                token = _bytetypes[1000][index - 1][0] if index > 0 else 'byte'
                multi = _bytetoken(token)[0]
                if index > 0: value = value / math.pow(1000, index)
            else:
                multi, token = 8, 'byte'
        else:
            multi, token = _bytetoken(token)
        try: self = float.__new__(cls, value, *argsv, **argsk)
        except: self = float.__new__(cls, 0, *argsv, **argsk)
        self.multi, self.token = multi, token
        return self
