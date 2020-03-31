########################################################
## Module  : Interpreter   ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import imp, os, sys

# import local modules
from .Main import *
from . import Error, Open, String, Sys, Unique

########################################################
## ------- here starts the module definitions ------- ##
########################################################
class compiler:
    dir = Sys.home
    file = __file__

    # compile
    def realstr(self, string, reverse=False):
        if reverse:
            string = string.replace('\\\\/', '')
        else:
            for old, new in [('\\', '\\\\'), ('\n', '\\n'),  ('"', '\\"'), ("'", "\\'")]:
                string = string.replace(old, new)

        if self.noscript:
            for old, new in [('{', '\\['), ('}', '\\]')]:
                string = string.replace(*((new, old) if reverse else (old, new)))
        return string

    def realline(self, string, strip=False):
        if len(self.spaces) > 0:
            count = len(string) - len(string.lstrip())
            if not strip and self.spaces[-1] == -1: self.spaces[-1] = count
            if not strip and count >= self.spaces[-1]: return ('    ' * len(self.spaces)) + string[self.spaces[-1] : ] + '\n'
            elif not strip and self.spaces[-1] > count and count > 0: return ('    ' * len(self.spaces)) + (' ' * 4) + string[count : ] + '\n'
            else: return ('    ' * len(self.spaces)) + (string.strip() if strip else string) + '\n'
        else:
            return (string.strip() if strip else string) + '\n'

    def realecho(self, string, strip=False):
        if string.strip()[0 : 6] == '@from ' or string.strip()[0 : 8] == '@import ':
            self.script += self.realline("__INFILE__('''%s''')" % self.realstr(string.strip(), 1)[1 : ])
        elif string.strip()[0 : 5] == 'from ' or string.strip()[0 : 7] == 'import ':
            self.script += self.realline('__IMPORT__(\'%s\')' % self.realstr(string.strip(), 1))
        else:
            self.script += self.realline(self.realstr(string, 1), strip)

    def prepare(self):
        current = ''
        devolve = ''
        opened = ''
        status = 0
        toecho = self.noscript
        for i in self.real + '\n':
            current += i
            if toecho:
                if current[-5 : ] in ['<?py ', '<?py\n']:
                    if len(devolve) > 0 and devolve[-1 : ] != '\n': devolve += '\n'
                    devolve += "__ECHO__('%s')\n" % (self.realstr(current[ : -5]))
                    toecho = False
                    current = ''
            elif status == 0:
                if i in ['"', "'"]:
                    opened = i
                    status = 1
                    current = ''
                elif self.noscript and current[-4 : ] in [' ?> ', ' ?>\n', '\n?> ', '\n?>\n']:
                    toecho = True
                    current = ''
                    devolve = devolve[ : -3]
                else:
                    devolve += i
            else:
                if opened * 2 == current:
                    opened += current
                    current = ''
                elif len(current) == 2 and opened == current[0]:
                    devolve += opened + current
                    current = ''
                    opened = ''
                    status = 0
                elif len(current) >= 2 and current[-len(opened) : ] == opened:
                    devolve += "__STRING__(%s%s%s)" % (opened, self.realstr(current[ : -len(opened)]), opened)
                    current = ''
                    opened = ''
                    status = 0
        if self.noscript and current != '\n':
            devolve += "\n__ECHO__('%s')\n" % (self.realstr(current))
        return devolve

    def compile(self, string):
        lcount = 0
        rcount = 0
        for line in string.splitlines():
            trim = String.trim(line)
            if trim != '':
                if self.noscript:
                    if trim[0 : 1] == '#':
                        self.script += self.realline(line, 1)
                    elif trim[0 : 6] == '@from ' or trim[0 : 8] == '@import ':
                        self.script += self.realline("%s__INFILE__('''%s''')" % (' ' * String.countrim(line)[0], trim[1 : ]))
                    elif trim[0 : 5] == 'from ' or trim[0 : 7] == 'import ':
                        self.script += self.realline('%s__IMPORT__(\'%s\')' % (' ' * String.countrim(line)[0], trim))
                    else:
                        name = ''.join(trim.split(' ')[ : 1])
                        if name in ['class', 'def', 'else', 'elif', 'except', 'finally', 'for', 'if', 'while', 'try'] and trim[-3 : ] != ': {' and trim[-1 : ] == '{':
                            self.script += self.realline(self.realstr(line.rstrip()[ : -1] + ':'))
                            self.spaces.append(-1)
                        else:
                            lcount += line.count('{')
                            rcount += line.count('}')
                            if len(self.spaces) > 0:
                                if rcount > lcount:
                                    leftover = rcount - lcount
                                    check = leftover - len(self.spaces)
                                    count = 0
                                    split = line.split('}')
                                    t=''
                                    for s in split:
                                        if len(split) - 1 > count:
                                            if len(self.spaces) > 0 and (check + 1 >= count if check > -1 else count >= (len(split) - leftover) - 1):
                                                if s.strip() != '':
                                                    self.realecho(s, 1)
                                                del self.spaces[-1]
                                                rcount -= 1
                                            else:
                                                t += s + '}'
                                        else:
                                            self.realecho(t + s, 1)
                                        count += 1
                                else:
                                    self.realecho(line)
                            else:
                                self.realecho(line)
                else:
                    if trim[0 : 6] == '@from ' or trim[0 : 8] == '@import ':
                        self.script += "%s__INFILE__('''%s''')\n" % (' ' * String.countrim(line)[0], trim[1 : ])
                    elif trim[0 : 5] == 'from ' or trim[0 : 7] == 'import ':
                        self.script += '%s__IMPORT__(\'%s\')\n' % (' ' * String.countrim(line)[0], trim)
                    else:
                        self.script += line + '\n'

    def setlocal(self):
        self.globals.update({
            # file
            '__dir__': self.dir,
            '__file__': self.file,
            # script
            'include': self.include,
            'require': self.require,
            '__import__': self.import_name,
            '__IMPORT__': self.import_head,
            '__INFILE__': self.import_file,
            # string
            'echo': self.echo,
            '__ECHO__': lambda string: self.echo(string, isfuncition=True),
            '__STRING__': lambda string: String.repvars(string, self.globals)
        })
        os.chdir(self.dir)

    # include
    def echo(self, *argsv, **argsk):
        string = ''
        count = 0
        for i in argsv:
            if count > 0 and not string[-1 : ] in ['\n', '\r']:
                string += ' '
            string += str(i)
            count += 1
        string = String.repvars(string, self.globals)
        if argsk.get('isfuncition') == True: string = String.repfunc(string, self.globals)
        self.string += string

    def include(self, file):
        self.string += compiler(file=file, globals=self.globals, mode='include').string
        self.setlocal()

    def require(self, file):
        self.string += compiler(file=file, globals=self.globals, mode='require').string
        self.setlocal()

    # import
    def import_error(self, error, **argsk):
        self.string += '\n%s\n' % (Error('import', error.args[0], **argsk))

    def import_pass(self):
        if self.allow == None: self.allow = Sys.allowAppCheck(self.id)
        return self.allow

    def import_file(self, head):
        type = head[ : head.find(' ')]
        file = head[head.find('\'') + 1 : head.rfind('\'')]
        end = head[head.rfind('\'') + 1 : ]
        try:
            file = os.path.realpath(file)
            os.chdir(os.path.dirname(file))
            module = imp.new_module(file)
            module.__file__ = file
            exec(open(file, 'r').read(), module.__dict__)
            if type == 'from':
                for item in end[end.find(' import ') + 8 : ].split(','):
                    split = item.split(' as ')
                    self.globals[split[1].strip() if len(split) > 1 else split[0].strip()] = module.__dict__[split[0].strip()]
            else:
                split = end.split(' as ')
                filename, extension = os.path.splitext(os.path.basename(file))
                self.globals[split[1].strip() if len(split) > 1 else split[0].strip()] = module
            self.setlocal()
        except Exception as error:
            self.import_error(error, file=file)

    def import_head(self, head):
        if self.import_pass():
            try: exec(head, self.globals)
            except Exception as error: self.import_error(error)

    def import_name(self, *argsv, **argsk):
        if self.import_pass():
            try: return __import__(*argsv, **argsk)
            except Exception as error: self.import_error(error)

    # running
    def running(self):
        self.setlocal()
        if 1:
            exec(self.script, self.globals, self.globals)
        else:
            try:
                exec(self.script, self.globals, self.globals)
            except Exception as e:
                try:
                    if self.mode == 'interpreter': error = Error(self.mode, type=e.msg, line=e.lineno, text=e.text)
                    else: error = Error(self.mode, type=e.msg, line=e.lineno, text=e.text, file=self.file)
                except:
                    if self.mode == 'interpreter': error = Error(self.mode, e.args[0])
                    else: error = Error(self.mode, e.args[0], file=self.file)
                self.string += '\n%s\n' % (error)

    def __init__(self, **argsk):
        self.allow = None
        self.globals = argsk.get('globals') if isinstance(argsk.get('globals'), dict) else {}
        self.id = argsk.get('id') if isinstance(argsk.get('id'), str) else Unique.id()
        self.mode = argsk.get('mode') if isinstance(argsk.get('mode'), str) else 'interpreter'
        self.noscript = not self.mode in ['require', 'script']
        self.script = ''
        self.spaces = []
        self.string = ''
        if isinstance(argsk.get('file'), str):
            self.file = os.path.realpath(argsk.get('file'))
            self.dir = os.path.dirname(self.file)
            if mode.lower() == 'interpreter':
                self.noscript = not os.path.splitext(self.file)[1].lower() in ['.py', '.pyh']
            try:
                string = Open.open(self.file).read()
            except:
                string = ''
                self.string = str(Error(self.mode, 'File not found', file=self.file))
        elif isinstance(argsk.get('string'), str): string = argsk.get('string')
        else: string = ''
        self.real = string
        if string != '':
            if self.noscript: self.compile(self.prepare())
            else: self.script = self.prepare()
            self.running()

class new:
    pass

setModule(__name__, '__call__', new)
