########################################################
## Module  : String        ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import re, unicodedata

# import local modules
from . import Class, Array

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def combine(keys, vals):
    count, devolve = 0, Array.new()
    for k in keys:
        try: devolve[k] = vals[count]
        except: devolve[k] = ''
        count += 1
    return devolve

def pad(self, repeat=5, char='*', toright=False):
    devolve, string = '',  str(self)
    count = repeat - len(string)
    if not toright: devolve += string
    if count > 0: devolve += char * count
    if toright: devolve += string
    return devolve

def swap(self, keys, vals=None, reverse=False):
    if isinstance(keys, str): array = combine(keys, vals)
    if Array.iskeys(array):
        if reverse: Array.key2val(array)
        for old, new in Array.items(array): self = self.replace(old, new)
    return self

def countrim(self):
    left, right = 0, 0
    for i in self:
        if i == ' ': left += 1
        else: break
    for i in reversed(self):
        if i == ' ': right += 1
        else: break
    return left, right

def alphaclear(self, empty=''):
    old = 'áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÖÔÚÙÛÜÇ'
    new = 'aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC'
    return re.sub(u'[^a-zA-Z0-9 ]', empty, swap(trim(self), old, new)).lower()

def link(self):
    regex = re.match('^([a-zA-Z]+[a-zA-Z0-9]+)://\S', self)
    if regex: return regex.string.split('://')[0]

def typeof(self):
    if self.isalpha(): return 'alpha'
    elif self.isnumeric(): return 'number'
    elif self.isalnum(): return 'alpha+number'
    elif re.match('^\d+\.\d+$', self): return 'float'
    elif re.match('^[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+$', self): return 'mail'
    elif re.match('^(/.*)+$', self): return 'path'
    elif re.match('^(?:file|(http|ftp)s?)://\S', self): return 'url'
    elif re.match('^([a-zA-Z]+[a-zA-Z0-9]+)://\S', self): return 'link'
    elif self.lower() in ['false', 'true']: return 'boolean'
    elif self.lower() in ['none', 'null', 'undefined']: return 'none'
    else: return 'string'

# parser
def query(self):
    # return
    items = ()
    end = '%v'
    ignore = ()
    # get
    ignored = False
    prev = ''
    string = ''

    for s in self:
        if s == '(':
            if prev != '\\' and not ignored:
                ignored = True

                if len(string) > 0:
                    item = string[0 : len(string)]
                    end = item
                    items += (item, )
                    string = ''

            else:
                string = string[0 : -1] + s

        elif s == ')':
            if  prev != '\\' and ignored:
                if string.count('%k') > 1 or string.count('%v') > 1 or (string.count('%k') == string.count('%v') == 1):
                    ii, ig, end = query(string.replace('(', '\(').replace(')', '\)'))
                    ig = list(ig)

                    if len(ii) > 1 and not ii[0] in ['%k', '%v']:
                        ig[0] = ii[0], ''

                    if  len(ii) > 1 and not ii[-1] in ['%k', '%v']:
                        ig[-1] = '', ii[-1]

                    items += tuple(list(ii)[1 : -1])
                    ignore += tuple(ig)

                elif string.find('%k') != -1:
                    end = '%k'
                    items += ('%k', )
                    ignore += (tuple(string.split('%k')), )

                else:
                    end = '%v'
                    items += ('%v', )
                    ignore += (tuple(string.split('%v')), )

                ignored = False
                string = ''

            else:
                string = string[0 : -1] + s

        elif not ignored:
            item = string[-2 : len(string)]

            if item in ['%k', '%v']:
                if len(string) > 2:
                    items += (string[0 : -2], )

                items += (item, )
                end = item
                ignore += (('', ''), )
                string = ''

            string += s

        else:
            string += s

        prev = s

    if len(string) > 0:
        items += (string, )

    else:
        items += (',', )

    return items, ignore, end

def split(self, iquery, call=None):
    devolve = Array.new()
    closed = False

    # item
    string = ''
    key = ''
    value = ''

    # query
    items, ignore, end = query(iquery)
    length = len(items) - 1
    close = items[length]

    # split
    count = 0
    current = items[0]
    next = items[1]
    prev = current
    ignored = ignore[0]

    for s in self + close:
        string += s

        if string[-len(close) : ] == close:
            closed = True
            prev = end
            value = string[0 : len(string) - len(close)]

        elif string[-len(next) : ] == next:
            prev = current
            value = string[0 : len(string) - len(next)]

            # split
            count += 2
            current = items[count]
            next = items[count + 1]

        if value != '':
            i1, i2 = ignored

            if len(i1) > 0 and value[0 : len(i1)] == i1:
                value = value[len(i1) : ]

            if len(i2) > 0 and value[-len(i2) : ] == i2:
                value = value[0 : -len(i2)]

            if key == '' and prev == '%k':
                key = Class.replace(call, value)
                devolve[value] = ''

            else:
                if key != '':
                    devolve[key] = Class.replace(call, value)

                else:
                    devolve += Class.replace(call, value)

            string = ''
            value = ''
            ignored = ignore[round(count / 2)]

        if closed:
            closed = False
            # item
            key = ''
            # split
            count = 0
            current = items[0]
            next = items[1]
            prev = current

    return devolve

def join(self, iquery, call=None):
    devolve = ''
    items, ignore, end = query(iquery)

    if Array.isarray(call):
        call = Array.totuple(call) + (str, )

    else:
        call = str

    for k, v in Array.items(self):
        addedkey = 0
        key = Class.replace(call, k)
        index = 0
        count = 0
        string = ''

        if Array.isarray(v):
            values = Class.replace(call, *Array.totuple(v))

        else:
            values = (Class.replace(call, v), )

        for i in items:
            if addedkey == 2:
                addedkey = 3
                string = ''

            elif i in ['%k', '%v']:
                ignored = ignore[count]

                if i == '%k' and not addedkey:
                    if not isinstance(self, dict) and isinstance(k, int):
                        addedkey = 2

                    else:
                        addedkey = 1
                        string += ignored[0] + key + ignored[1]

                else:
                    try:
                        value = values[index]

                    except:
                        value = ''

                    index += 1

                    if addedkey == 1:
                        string += ignored[0] + value + ignored[1]

                    else:
                        string += value

                count += 1

            else:
                string += i

        devolve += string

    return devolve[0 : -len(items[-1])]

# find
def find(self, key):
    devolve = None
    items = list(re.finditer(key, self))

    if len(items) > 0:
        devolve = Array.new()

        for i in items:
            item = Array.new(i.span())
            item += re.findall(key, i.group())[0]
            devolve += item

    return devolve

def rfind(self, query, index=1):
    return len(query.join(self.split(query)[ : -index]))

def lfind(self, query, index=1):
    return len(query.join(self.split(query)[ : index]))

# replace
def repvars(self, vars={}):
    for real, path in re.findall('(\$\{(.*?)\})', self):
        try:
            count, points = 0, path.split('.')
            for var in points:
                value = Array.todict(vars)[var] if count == 0 else Array.todict(value)[var]
                if count == len(points) - 1: self = self.replace(real, str(value))
                count += 1
        except:
            pass
    return self

def repfunc(self, vars={}):
    for item in re.findall('(\$\(([\d\w_. ]+)\))', self) + re.findall('(\$\((.*?) [\'|\"]+(.*?)[\'|\"]+\))', self):
        try:
            real, path, value = item
        except:
            real, path = item
            value = None
        try:
            countSpace = 0
            for space in reversed(path.split(' ')):
                countPoint = 0
                for var in space.split('.'):
                    if countPoint == 0:
                        try: func = vars[var]
                        except: func = Array.todict(__builtins__)[var]
                    else:
                        func = Array.todict(func)[var]
                    countPoint += 1
                value = func() if countSpace == 0 and value == None else func(value)
                countSpace += 1
            self = self.replace(real, str(value))
        except:
            pass
    return self

def replace(self, vars={}):
    self = repvars(self, vars)
    self = repfunc(self, vars)
    return self

# format
def format(self, items, end=True):
    index, length, string = 1, len(items), ''
    for i in items:
        if end or length > index: string += self % i
        else: string += i
        index += 1
    return string

# detect
def charDetect(self):
    return unicodedata.name(self, '').split()[0].lower()

def detect(self):
    devolve = []
    for char in self:devolve.append(charDetect(char))
    return tuple(set(devolve))
