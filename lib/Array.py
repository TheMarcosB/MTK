########################################################
## Module  : Array         ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
from collections import OrderedDict

# import local modules
from .Main import *
from . import Class, Error

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# check
def isadd(self):
    return isinstance(self, (dict, list, new))

def iskeys(self):
    return isinstance(self, (dict, new))

def islist(self):
    return isinstance(self, (list, tuple))

def iscount(self):
    devolve = True
    if not islist(self):
        count = 0
        for k, v in items(self):
            if not isinstance(k, int) or k != count:
                devolve = False
                break
            count += 1
    return devolve

def isarray(self):
    return islist(self) or iskeys(self)

# check error
def noadd(self):
    devolve = isadd(self)
    if not devolve: Error.new('array', 'Array can not be modified', In=self)
    return devolve

def noarray(self):
    devolve = isarray(self)
    if not devolve: Error.new('array', 'This is not an array', In=self)
    return devolve

def nokeys(self):
    devolve = iskeys(self)
    if not devolve: Error.new('array', 'Array does not exist key', In=self)
    return devolve

# items
def items(self, isall=False):
    if islist(self): return list(zip(range(len(self)), self))
    elif isinstance(self, dict): return list(self.items())
    elif isinstance(self, new): return self.__list__
    else: return [(i, Class.getattr(self, i)) for i in dir(self) if (isall or not i[0 : 2] == i[-2 : ] == '__')]

def keys(self, isall=False):
    if islist(self): return list(range(len(self)))
    elif isinstance(self, dict): return list(self.keys())
    else: return list(list(zip(*items(self, isall)))[0])

def values(self, isall=False):
    if isinstance(self, dict): return list(self.values())
    elif isinstance(self, list): return self
    elif islist(self): return list(self)
    else: return list(list(zip(*items(self, isall)))[1])

# real
def realvalue(value):
    try:
        if isinstance(value, (dict, list)):
            value = new(value)
    except:
        value = None
    return value

class realindex(int):
    def __repr__(self):
        return 'Index{' + str(self.real ) + '}'

    def __str__(self):
        return self.__repr__()

    def __new__(cls, key):
        return int.__new__(cls, key)

class realitem(tuple):
    def __contains__(self, check):
        return check in self[1]

# string
def string(self, isspace=True, space=''):
    devolve = 'Array('
    count = 1
    _items = items(self)
    length = len(_items)
    if isspace and length > 0: devolve += '\n'
    for k, v in _items:
        if isspace:
            devolve += space + (' ' * 4)
        devolve += repr(k) + '-> '
        count += 1
        if isadd(v): devolve += string(v, isspace, space + (' ' * 4))
        else: devolve += repr(v)
        if length >= count:
            if isspace: devolve += ',\n'
            else: devolve += ', '
    if isspace and length > 0: devolve += '\n' + space
    return devolve + ')'

def tostring(self, join=' '):
    devolve = ''
    count = 0
    length = len(self)
    for k, v in items(self):
        count += 1
        if isarray(v): devolve += tostring(v)
        else: devolve += str(v)
        if length > count: devolve += join
    return devolve

# check items
def index(self, compare, bykey=True):
    devolve = -1
    if noarray(self):
        count = 0
        try:
            if bykey and type(compare) is set and len(compare) == 1 and type(tuple(compare)[0]) is int:
                try:
                    key = tuple(compare)[0]
                    self.__list__[key]
                    devolve = key
                except:
                    pass
            else:
                for k, v in items(self):
                    _iskey = compare == k and isinstance(k, type(compare)) and not type(k) is realindex
                    _isval = compare == v and isinstance(v, type(compare))
                    if _iskey if bykey else _isval:
                        devolve = count
                        break
                    count += 1
        except:
            Error.alert('array', 'failed', Function='index', In=self)
    return devolve

def inkey(self, key): # index by key
    return index(self, key, True)

def inval(self, value): # index by value
    return index(self, value, False)

def iskey(self, key): # key exists
    return inkey(self, key) > -1

def isval(self, value): # value exists
    return inval(self, value) > -1

# delete items
def clear(self):
    if noadd(self):
        try:
            if isinstance(self, new): self.__list__.clear()
            else: self.clear()
            return True
        except:
            Error.alert('array', 'failed', Function='clear', In=self)
    return False

def delkey(self, *keys): # by key
    if noadd(self):
        try:
            _int = ()
            _str = ()
            for key in keys:
                if isinstance(key, str): _str += key,
                else: _int += key,
            for key in tuple(sorted(_int, reverse=True)) + _str:
                try: del self[key]
                except: pass
        except:
            Error.alert('array', 'failed', Function='delkey', In=self)
    return self

def delval(self, *values): # by value
    if noadd(self):
        try:
            delete = ()
            for k, v in items(self):
                if v in values: delete += k,
            delkey(self, *delete)
        except:
            Error.alert('array', 'failed', Function='delval', In=self)
    return self

# update array
def append(self, *argsv):
    if noadd(self):
        try:
            count = len(self)
            for value in argsv:
                if isinstance(self, dict): self[count] = value
                elif isinstance(self, list): self.append(value)
                else: self.__list__.append(realitem((realindex(count) if iskey(self, count) else count, realvalue(value))))
                count += 1
            return True
        except:
            Error.alert('array', 'failed', Function='append', In=self, Value=argsv)
    return False

def add(self, array):
    append(self, *values(array))

def update(self, merge, isall=False, isitems=False):
    if noadd(self):
        try:
            for key, value in (merge if isitems else items(merge, isall)):
                if isinstance(self, list) and not isitems:
                    append(self, value)
                else:
                    if islist(merge) and not isitems: append(self, value)
                    elif type(key) is realindex and isinstance(self, new) and isinstance(merge, new): append(self, value)
                    else:
                        if isinstance(self, new): value = realvalue(value)
                        self[key] = value
            return True
        except:
            Error.alert('array', 'failed', Function='update', In=self, Value=merge)
    return False

# orders for array
def key2val(self):
    try:
        if nokeys(self):
            copied = items(self).copy()
            if clear(self):
                for k, v in copied:
                    self[v] = k
    except:
        Error.alert('array', 'failed', Function='key2val', In=self)
    return self

def reverse(self):
    try:
        copied = items(self).copy()
        if noadd(self) and clear(self): update(self, reversed(copied), isitems=True)
    except:
        Error.alert('array', 'failed', Function='reverse', In=self)
    return self

def sort(self, order=False, bykeys=None, nokeys=None):
    if noadd(self):
        try:
            if len(self) > 0:
                array = OrderedDict()
                count = 0
                _keys = keys(self)
                _values = values(self)
                _sort = []
                for value in _values:
                    if isarray(value):
                        if bykeys or nokeys:
                            query = ''
                            for k, v in items(nokeys):
                                if iskey(value, k):
                                    query += str(v)
                            _sort.append((query, count))
                        else:
                            _sort.append((tostring(values(value)), count))
                    else:
                        _sort.append((str(value), count))
                    count += 1
                for query, index in sorted(_sort, reverse=order):
                    value = _values[index]
                    key = _keys[index]
                    array[key] = value
                if clear(self): update(self, array)
        except:
            Error.alert('array', 'failed', Function='sort', In=self)
    return self

# equal
def equal(self, compare):
    if noarray(self):
        try:
            if isarray(compare) and len(self) == len(compare):
                devolve = True
                compare = items(compare)
                count = 0
                for k, v in items(self):
                    i = compare[count]
                    if k != i[0] and not (islist(self) or islist(compare)):
                        devolve = False
                    elif isarray(v):
                        if isarray(i[1]): devolve = equal(v, i[1])
                        else: devolve = False
                    elif v != i[1]:
                        devolve = False
                    if not devolve: break
                    count += 1
                return devolve
        except:
            Error.alert('array', 'failed', Function='equal', In=self)
    return False

# search
def _search(query, value):
    devolve = True
    for k, v in items(query):
        try:
            if isarray(v) and isarray(value[k]):
                if len(value[k]) > 0:
                    for i in values(v):
                        devolve = False
                        for item in values(value[k]):
                            if str(i).lower() == str(item).lower():
                                devolve = True
                                break
                        if not devolve:
                            break
                else:
                    devolve = False
            elif str(v).lower() != str(value[k]).lower():
                devolve = False
        except:
            devolve = False
            break
    return devolve

def search(self, query):
    devolve = []
    for key, value in items(self):
        try:
            if isarray(value):
                if isinstance(query, str) and query.lower() in tostring(value).lower():
                    devolve.append((key, value))
                elif isinstance(query, (dict, new)):
                    if _search(query, value): devolve.append((key, value))
                elif isinstance(query, (tuple, list)) and query[0].lower() in tostring(value).lower():
                    if _search(query[1], value): devolve.append((key, value))
            elif isinstance(query, (float, int, str)) and str(query).lower() in str(value).lower():
                devolve.append((key, value))
        except:
            pass
    return devolve

# create new array
class new:
    # attribute
    def __delattr__(self, key): # del delete.key
        if Class.delattr(self, key): return True
        else: return self.__delitem__(key)

    def __getattr__(self, key): # get.key
        if Class.isattr(self, key): return Class.getattr(self, key)
        else: return self.__getitem__(key)

    def __setattr__(self, key, value): # update.key = value
        if Class.isattr(self, key): Class.setattr(self, key, value)
        else: self.__setitem__(key, value)

    # item
    def __delitem__(self, key): # del delete[key]
        try:
            if type(key) is set and len(key) == 1 and type(tuple(key)[0]) is int: key = tuple(key)[0]
            else: key = inkey(self, key)
            del self.__list__[key]
            return True
        except:
            return False

    def __getitem__(self, key): # get[key]
        devolve = None
        if type(key) is slice:
            try: return new(self.__list__[key], isitems=True)
            except: return new()
        elif type(key) is set and len(key) == 1 and type(tuple(key)[0]) is int:
            try: devolve = self.__list__[tuple(key)[0]][1]
            except: pass
        else:
            for k, v in self.__list__:
                if key == k and isinstance(k, type(key)) and not type(k) is realindex:
                    devolve = v
                    break
        return devolve

    def __setitem__(self, key, value): # update[key] = value
        value = realvalue(value)
        if type(key) is set and len(key) == 1 and type(tuple(key)[0]) is int:
            key = tuple(key)[0]
            try:
                k, v = self.__list__[key]
                self.__list__[key] = realitem((k, value))
            except:
                if key == len(self):
                    self.__list__.append(realitem((realindex(key) if iskey(self, key) else key, value)))
        else:
            added = False
            count = 0
            for k, v in self.__list__:
                if k == key and isinstance(k, type(key)) and not type(k) is realindex:
                    added = True
                    self.__list__[count] = realitem((key, value))
                    break
                count += 1
            if not added:
                self.__list__.append(realitem((key, value)))

    # list
    def __iter__(self):
        return self.__list__.__iter__()

    def __len__(self):
        return self.__list__.__len__()

    def __next__(self):
        return self.__list__.__next__()

    # update
    def __add__(self, array): # self + update
        update(self, array)
        return self

    def __iadd__(self, value): # append += value
        append(self, value)
        return self

    def __mod__(self, query):
        return new(search(self, query), isitems=True)

    def __isub__(self, argsv): # delete by -= keys
        try: delkey(self, *argsv)
        except: delkey(self, argsv)
        return self

    # check
    def __bool__(self):
        return bool(len(self.__list__) > 0)

    def __contains__(self, check):
        return check in values(self)

    def __eq__(self, compare):
        return equal(self, compare)

    def __ne__(self, compare):
        return not equal(self, compare)

    # string
    def __repr__(self):
        return string(self, False)

    __str__ = __repr__

    # array
    def __call__(self, index, item=1):
        try: return self.__list__[index][item]
        except: pass

    def __new__(cls, merge=None, *argsv, isall=False, isitems=False, **argsk):
        self = object.__new__(cls)
        Class.setattr(self, '__list__', [])
        if merge != None: update(self, merge, isall, isitems)
        return self

class blocker(new, Class.new):
    def __new__(cls, merge=None, *argsv, **argsk):
        self = Class.new.__new__(cls, *argsv, **argsk)
        if merge: update(self, merge)
        return self

# array convert
def todict(self): # dict
    if not isinstance(self, dict): return dict(items(self))
    else: return self

def toarray(self): # array
    if not isinstance(self, new): return new(items(self), istems=True)
    else: return self

def tolist(self): # list
    if not isinstance(self, list): return list(values(self))
    else: return self

def totuple(self): # tuple
    if not isinstance(self, tuple): return tuple(values(self))
    else: return self

# array copy
def copy(self):
    try:
        if isinstance(self, new):
            array = new()
            for k, v in self.__list__:
                if isinstance(v, new): v = copy(v)
                array.__list__.append((k, v))
            return array
        else:
            return self.copy()
    except:
        pass

# modify array with path
def path(self, pathlist, *argsv, **argsk):
    if noarray(self):
        try:
            keylist = argsk.keys()
            length = len(pathlist)
            if length > 0:
                count = 0
                devolve = None
                for i in pathlist:
                    count += 1
                    if count == length:
                        if 'new' in keylist: self[i] = argsk['new']
                        elif 'add' in keylist: self[i] += argsk['add']
                        elif 'sub' in keylist: self[i] -= argsk['sub']
                        elif 'mul' in keylist: self[i] *= argsk['mul']
                        elif 'div' in keylist: self[i] /= argsk['div']
                        else: devolve = self[i]
                    else:
                        self = self[i]
                return devolve
            else:
                return self
        except:
            Error.alert('array', 'failed', Function='path', In=self)
    return None

# end module
setModule(__name__, '__call__', new)
