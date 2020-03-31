########################################################
## Module  : Url           ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import os, re, ssl, socket, sys

# import local modules
from . import Array, Code, Json, Open, String, Time

# fixed variables
version = 1.0
_url_protocols = Json.sys('url-protocols')
_url_status = Json.sys('url-status')

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def check(string):
    return bool(re.search('(^[a-zA-z]+[a-zA-z0-9]+://(.*?))$', string))

def header_parse(string):
    count = 0
    devolve = {}

    for line in string.split('\r\n'):
        try:
            key, value = line.split(': ')
            devolve[key] = value

        except:
            devolve[count] = line
            count += 1

    return devolve

# split
def split(url, index=None):
    try:
        items = url.split('/')
        _scheme = items[0][0 : -1].lower()
        _uri = None

        if items[2].find('?') != -1:
            _site, _uri = items[2].split('?')

        else:
            _site = items[2]

        _host = _site.split(':')
        _port = 80

        try: _port = _url_protocols[_scheme]
        except: pass

        if len(_host) > 1:
            _port = int(_host[1])

        if not _uri:
            _uri = '/' + '/'.join(items[3 : ])

        else:
            _uri = '?' + _uri

        devolve = _scheme, _site, _host[0], _port, _uri

        if isinstance(index, int):
            return devolve[index]

        else:
            return devolve

    except:
        return None

def scheme(url):
    return split(url, 0)

def site(url):
    return split(url, 1)

def host(url):
    return split(url, 2)

def port(url):
    return split(url, 3)

def protocol(string):
    try:
        if check(string):
            string = scheme(string)

        return _url_protocols[string]

    except:
        pass

def uri(url):
    return split(url, 4)

# coding
def decode(string):
    return Code.quote_decode(string, {'+': ' '})

def encode(string):
    return Code.quote_encode(string, {' ': '+'}, '.-_')

# bar
def bar(url):
    return '/' + uri(url).split('?')[0]

def bar_parse(url):
    return bar(url).split('/')[1 : ]

def bar_up(url, *vals, **keys):
    pass

# get
def get(url):
    try:
        return '?' + uri(url).split('?')[1]

    except:
        return ''

def get_join(array):
    return String.join(array, '%k=%v&', call=encode)

def get_parse(string):
    if check(string):
        string = get(string)[1 : ]

    return String.split(string, '%k=%k&', call=decode)

def get_up(url, *vals, **keys):
    pass

# status
def get_status(code):
    return _url_status[str(code)]

def status_info(code):
    return get_status(code)[0]

def status_full(code):
    return get_status(code)[1]

class status_code(int):
    def info(self):
        if self.alt:
            return self.alt

        else:
            return status_info(self)

    def full(self):
        if self.alt:
            return self.alt

        else:
            return status_full(self)

    def __init__(self, code, alt=None):
        self.alt = alt

# data
def opensplit(url, method='GET', header={}, context='', justhead=False, redirect=True, time=1):
    _head = ''
    _header = {}
    _status = status_code(0)
    _location = None
    _length = None
    _content = ''

    try:
        # connect
        _scheme, _link, _host, _port, _uri = split(url)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((_host, _port))
        sock.settimeout(time)

        if _scheme == 'https':
            sock = ssl.wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

        # client
        data = None
        send = ''
        string = ''
        headers = {
           0: '%s %s HTTP/1.1' % (method, _uri),
           'Host': _host,
           'User-Agent': 'TheMarcosUrl/' + str(version),
           'Accept': '*/*',
           'Data': Time.web(),
           'Content-Length': len(context),
           'Connection': 'close'
        }

        try: headers.update(header)
        except: pass

        for key, value in headers.items():
            if isinstance(key, int):
                send += str(value) + '\r\n'

            else:
                send += '{}: {}\r\n'.format(str(key), str(value))

        send += '\r\n' + context
        sock.sendall(send.encode('ISO-8859-1'))

        # content
        while True:
            try:
                part = sock.recv(1024)

                if not part or part == b'':
                    break

                if not data:
                    string += part.decode('ISO-8859-1')

                    if string.find('\r\n\r\n') != -1:
                        data = string.split('\r\n\r\n')
                        _head = data[0]
                        _content = '\r\n\r\n'.join(data[1 : ])
                        _header = header_parse(_head)

                        try: _status = status_code(int(re.findall('HTTP/1.1 (\d+) ', _header[0])[0]))
                        except: _status = status_code(200)
                        try: _length = round(float(_header['Content-Length']))
                        except: pass
                        try: _location = _header['Location']
                        except: pass

                        if justhead:
                            break

                else:
                    _content += part.decode('ISO-8859-1')

                if _length == 0 or (_length and len(_content) >= _length):
                    break

            except:
                break

        sock.close()

    except Exception as error:
        try:
            error = re.findall('\[Errno (.*?)\] ([\d \S]+)', str(error))[0]
            _status = status_code(int(error[0]), error[1])

        except:
            pass

    # length
    if not _length:
        _length = len(_content)

    if redirect and _location and redirect != _location:
        _head, _header, _status, _location, _length, _content = opensplit(_location, method=method, header=header, context=context, justhead=justhead, redirect=_location, time=time)

    elif isinstance(redirect, str):
        _location = redirect

    else:
        _location = url

    return _head, _header, _status, _location, _length, _content

class open:
    def bytes(self):
        return self.content.encode('ISO-8859-1')

    def save(self, path=os.getcwd()):

            filname = self.disposition['filename']

            if not filname:
                filname = bar_parse(self.location)[-1]

            if not filname:
                filname = 'test.html'

            Open.write('%s/%s' % (path, filname), *((self.content, 'w') if self.type == 'text' else (self.bytes(), 'wb')))

    def __new__(cls, url, **keys):
        self = object.__new__(cls)
        self.head, self.header, self.status, self.location, self.length, self.content = opensplit(url, **keys)
        self.exists = self.status > 0
        self.mime = 'undefined'

        try:
            self.mime = re.findall('([-\d.A-z]+/[-\d.A-z]+)', self.header['Content-Type'])[0]

        except:
            if self.status != 404:
                self.mime = 'application/octet-stream'

        try:
            self.disposition = String.split(self.header['Content-Disposition'], '%k=("%v"); ', decode)

        except:
            self.disposition = Array.new()

        self.type = self.mime.split('/')[0]
        return self

def head(url, **keys):
    return opensplit(url, justhead=True, **keys)[0]

def header(url, **keys):
    return opensplit(url, justhead=True, **keys)[1]

def status(url, **keys):
    return opensplit(url, justhead=True, **keys)[2]

def exists(url, **keys):
    return status(url, **keys) > 0

def location(url, **keys):
    return opensplit(url, justhead=True, **keys)[3]

def length(url, **keys):
    return opensplit(url, justhead=True, **keys)[4]

def mime(url, **keys):
    data = opensplit(url, justhead=True, **keys)
    devolve = 'undefined'

    try:
        devolve = re.findall('([-\d.A-z]+/[-\d.A-z]+)', data[1]['Content-Type'])[0]

    except:
        if data[2] != 404:
            devolve = 'application/octet-stream'

    return devolve

def type(url, **keys):
    return mime(url, **keys).split('/')[0]

def content(url, **keys):
    return opensplit(url, **keys)[5]

def bytes(url, **keys):
    return content(url, **keys).encode('ISO-8859-1')

# send
def sendpost(url, posts, **keys):
    context = get_join(posts)
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    return open(url, **keys, method='PUT', header=header, context=context)
