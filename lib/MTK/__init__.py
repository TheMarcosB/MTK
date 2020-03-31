#########################################################
## Module  : MTK            ## Author   : Marcos Bento ##
## ------------------------ ## ----------------------- ##
## Github  : TheMarcosBC    ## Twitter  : TheMarcosBC  ##
## ------------------------ ## ----------------------- ##
## Facebook: TheMarcosBC    ## Instagram: TheMarcosBC  ##
#########################################################

# import default modules
import time as _time

# import local modules
from . import Event as _event, Get as _get, Tags as _tags, Update as _update
from .Variables import *
from ..Main import Object as _object

# fixed variables
window = _tags.Window

#########################################################
## -------- here starts the module definitions ------- ##
#########################################################
# loop
class _events:
    widget = '.'

def _timer():
    tk = _get.getTk(_tags.Window.main)
    for window in _tags.Windows:
        data, (x, y)= _get.getData(window), window.pointer
        for loop in _object.get(window, '__loop__'): _event.Timer(loop)
        for timeout in _object.get(window, '__timeout__'): _event.Timer(timeout)
        for interval in _object.get(window, '__interval__'): _event.Timer(interval)
        if not data.get('cursor') or data.get('cursor') != (x, y):
            event = _events()
            event.x_root, event.y_root = x, y
            Event.Command(event, window, 'cursor')
            data['cursor'] = x, y
        updateTime = data.get('update-time')
        if not updateTime or _time.time() - updateTime >= 0.1:
            updateLoop = data.get('update-loop')
            if not updateLoop or _time.time() - updateLoop >= 0.01:
                _update.up(window)
                data['update-loop'] = _time.time()
    tk.after(1, _timer)

def loop():
    main = _tags.Window.main
    if main:
        tk = _get.getTk(main)
        tk.after(1, _timer)
        tk.mainloop()

def loop2():
    tk = _get.getTk(_tags.Window.main)
    while True:
        for window in _tags.Windows:
            data, (x, y)= _get.getData(window), window.pointer
            for loop in _object.get(window, '__loop__'): _event.Timer(loop)
            for timeout in _object.get(window, '__timeout__'): _event.Timer(timeout)
            for interval in _object.get(window, '__interval__'): _event.Timer(interval)
            if not data.get('cursor') or data.get('cursor') != (x, y):
                event = _events()
                event.x_root, event.y_root = x, y
                Event.Command(event, window, 'cursor')
                data['cursor'] = x, y
            updateTime = data.get('update-time')
            if not updateTime or _time.time() - updateTime >= 0.1:
                updateLoop = data.get('update-loop')
                if not updateLoop or _time.time() - updateLoop >= 0.01:
                    _update.up(window)
                    data['update-loop'] = _time.time()
        tk.update()
