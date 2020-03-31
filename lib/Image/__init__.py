###################################################################
## Module  : Image             ## Author   : Marcos Bento        ##
## --------------------------- ## ------------------------------ ##
## Github  : TheMarcosBC       ## Twitter  : TheMarcosBC         ##
## --------------------------- ## ------------------------------ ##
## Facebook: TheMarcosBC       ## Instagram: TheMarcosBC         ##
###################################################################

# import default modules
import io, math, os
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps, ImageTk

# import local modules
from . import Color
from .. import Error
from ..Main import *

###################################################################
## ------------ here starts the module definitions ------------- ##
## start ##########################################################
def _upsize(self, size):
    self._size, self._padding = size, (0, 0, 0, 0)
    self._border, self._corners  = (0, 0, 0, 0), None
    self._position, self._shadow = [0, 0], (0, 0)

# corners
def getcorners(values):
    corners = []
    for i in range(4):
        if isinstance(values, (float, int)):
            corners.append(round(values))
        else:
            try:
                try: corner = round(values[i])
                except: corner = round(values[1 if i == 3 else 0])
                corners.append(corner)
            except:
                if corners:
                    corners.append(corners[0])
                else:
                    corners = [0, 0, 0, 0]
                    break
    return tuple(corners)

def _corner(size, length, position):
    width, height = size
    rw, rh = length
    bw, bh = rw * 2, rh * 2
    new_image = Image.new('L', size, 255)
    draw = ImageDraw.Draw(new_image)
    draw.polygon([(0, 0), (rw, 0), (0, rh)], 0)
    draw.ellipse((0, 0, bw, bh), 255)
    if position == 'right': new_image = ImageOps.mirror(new_image)
    elif position == 'bottom': new_image = new_image.rotate(180)
    elif position == 'left': new_image = ImageOps.mirror(new_image.rotate(180))
    return new_image

def _calcorners(size, values):
    w, h = size
    dw, dh = w / 2, h / 2
    pw, ph = (w * 2) / math.pi, (h * 2) / math.pi
    t, r, b, l = values
    # top
    if t >= w or r >= w or (t >= dw and r >= dw): tw = round(pw * math.atan(t / max(r, 0.1)))
    else: tw = round(t)
    if t >= h or l >= h or (t >= dh and l >= dh): th = round(ph * math.atan(t / max(l, 0.1)))
    else: th = round(t)
    # right
    if r >= w or t >= w or (r >= dw and t >= dw): rw = round(pw * math.atan(r / max(t, 0.1)))
    else: rw = round(r)
    if r >= h or b >= h or (r >= dh and b >= dh): rh = round(ph * math.atan(r / max(b, 0.1)))
    else: rh = round(r)
    # bottom
    if b >= w or l >= w or (b >= dw and l >= dw): bw = round(pw * math.atan(b / max(l, 0.1)))
    else: bw = round(b)
    if b >= h or r >= h or (b >= dh and r >= dh): bh = round(ph * math.atan(b / max(r, 0.1)))
    else: bh = round(b)
    # left
    if l >= w or b >= w or (l >= dw and b >= dw): lw = round(pw * math.atan(l / max(b, 0.1)))
    else: lw = round(l)
    if l >= h or t >= h or (l >= dh and t >= dh): lh = round(ph * math.atan(l / max(t, 0.1)))
    else: lh = round(l)
    # devolve
    return (tw, th), (rw, rh), (bw, bh), (lw, lh)

def _cornersmask(size, corners, isrealcorners):
    # big size
    bigsize = round(size[0] * 3), round(size[1] * 3)
    # big corners
    if isrealcorners:
        ts, rs, bs, ls = corners
    else:
        bigcorners = corners[0] * 3, corners[1] * 3, corners[2] * 3, corners[3] * 3
        ts, rs, bs, ls = _calcorners(bigsize, bigcorners)
    # mask
    mask = Image.new('L', bigsize, 255)
    if ts[0] > 0 and ts[1] > 0: mask = ImageChops.difference(mask, _corner(bigsize, ts, 'top'))
    if rs[0] > 0 and rs[1] > 0: mask = ImageChops.difference(mask, _corner(bigsize, rs, 'right'))
    if bs[0] > 0 and bs[1] > 0: mask = ImageChops.difference(mask, _corner(bigsize, bs, 'bottom'))
    if ls[0] > 0 and ls[1] > 0: mask = ImageChops.difference(mask, _corner(bigsize, ls, 'left'))
    # devolve
    return mask.resize(size, Image.ANTIALIAS), (ts, rs, bs, ls), size, mask

def _newcorners(self, size):
    new_size = size[0] + size[1]
    old_size = self._corners[2][0] + self._corners[2][1]
    corners = []
    for width, height in self._corners[1]:
        if old_size > new_size:
            less = math.floor((old_size - new_size) / 1.5)
            width -= less
            height -= less
        else:
            more =  math.floor((new_size - old_size) / 1.5)
            width += more
            height += more
        corners.append((max(width, 0), max(height, 0)))
    return _cornersmask(size, tuple(corners), True)

def _cropcorners(self, size):
    crop = self._corners[3]
    new_image = Image.new('RGBA', (math.floor(size[0] * 3), math.floor(size[1] * 3)))
    new_image.paste(self._image.resize(crop.size), (0, 0), crop)
    self._image = new_image.resize(size, Image.ANTIALIAS)

def _upcorners(self, size):
    if self._corners:
        self._corners = _newcorners(self, size)
        _cropcorners(self, size)

def _crop(self, image):
    crop, size = self._corners[3], image.size
    image.resize(crop.size)
    return ImageChops.difference(image, crop).resize(size, Image.ANTIALIAS)

# create
class img:
    # background
    def append(self, image, x=0, y=0):
        bg = self._image.crop((x, y, image.size[0] + x, image.size[1] + y))
        self._image.paste(Image.alpha_composite(bg, image._image), (x, y))
        return self

    def canvas(self, items):
        if len(items) > 0:
            width, height = self.size
            canvas = Image.new('RGBA', (math.floor(width * 3), math.floor(height * 3)), Color.Transparent)
            draw = ImageDraw.Draw(canvas)
            for name, x, y, w, h, color, text in items:
                x, y, w, h = math.floor(x * 3), math.floor(y * 3), math.floor(w * 3), math.floor(h * 3)
                if name =='rectangle': draw.rectangle((x, y, x + w, y + h), color)
                elif name == 'ellipse': draw.ellipse((x, y, x + w, y + h), color)
            self._image = Image.alpha_composite(self._image, canvas.resize((width, height), Image.ANTIALIAS))

    def color(self, color):
        color, new_data = Color.new(color).rgb, []
        for r, g, b, a in self._image.getdata(): new_data.append(color + (a, ))
        self._image.putdata(new_data)

    def expand(self, *values):
        corners = getcorners(values)
        if corners != (0, 0, 0, 0):
            (w, h), (t, r, b, l) = self.size, corners
            new_size = math.floor(w + r + l), math.floor(h + t + b)
            new_image = Image.new('RGBA', new_size, self._color.rgba)
            new_image.paste(self._image, (t, l))
            self._image = new_image
            self._padding = t, r, b, l
            _upcorners(self, new_size)
        return self

    def fill(self, color):
        self._color = Color.new(color)
        new_image = Image.new('RGBA', self.size, self._color.rgba)
        self._image = Image.alpha_composite(new_image, self._image)
        return self

    def repeat(self, size, mode='normal', x=0, y=0):
        old_image, old_size = self._image, self._image.size
        if mode in ['loop-round', 'loop-stretch']:
            w2, h2 = math.floor(old_size[0] / 3), math.floor(old_size[1] / 3)
            w0, h0 = w2 * 3, h2 * 3
            xl, yl = math.floor(size[0] / w2), math.floor(size[1] / h2)
            w1, h1 = w2 * xl, h2 * yl
            # get image
            old_image = old_image.resize((w0, h0), Image.ANTIALIAS)
            new_image = Image.new('RGBA', (w1, h1))
            # get sides
            top = old_image.crop((w2, 0, w0 - w2, h2))
            right = old_image.crop((w0 - w2, h2, w0, h0 - h2))
            bottom = old_image.crop((w2, h0 - h2, w0 - w2, h0))
            left = old_image.crop((0, h2, w2, h0 - h2))
            # add sides
            if mode == 'loop-round':
                for x in range(xl - 2):
                    new_image.paste(top, (w2 * (x + 1), 0))
                    new_image.paste(bottom, (w2 * (x + 1), h1 - h2))
                for y in range(yl - 2):
                    new_image.paste(left , (0, h2 * (y + 1)))
                    new_image.paste(right, (w1 - w2, h2 * (y + 1)))
            else:
                new_image.paste(top.resize((w1 - (w2 * 2), h2), Image.ANTIALIAS), (w2, 0))
                new_image.paste(bottom.resize((w1 - (w2 * 2), h2), Image.ANTIALIAS), (w2, h1 - h2))
                new_image.paste(right.resize((w2, h1 - (h2 * 2)), Image.ANTIALIAS), (w1 - w2, h2))
                new_image.paste(left.resize((w2, h1 - (h2 * 2)), Image.ANTIALIAS), (0, h2))
            # corners
            new_image.paste(old_image.crop((0, 0, w2, h2)))
            new_image.paste(old_image.crop((w0 - w2, 0, w0, h2)), (w1 - w2, 0))
            new_image.paste(old_image.crop((w0 - w2, h0 - h2, w0, h0)), (w1 - w2, h1 - h2))
            new_image.paste(old_image.crop((0, h0 - h2, w2, h0)), (0, h1 - h2))
            copy = new_image.copy()
            w3, h3 = w1 - (w2 * 2), h1 - (h2 * 2)
            pw, ph = math.floor(w3 *(100 / w1)), math.floor(h3 *(100 / h1))
            while w3 > w0 and h3 > h0:
                new_image.paste(copy.resize((w3, h3), Image.ANTIALIAS), (math.floor((w1 - w3) / 2), math.floor((h1 - h3) / 2)))
                w3, h3 = math.floor((w3 / 100) * pw), math.floor((h3 / 100) * ph)
            new_image.paste(old_image.resize((w3, h3), Image.ANTIALIAS), (math.floor((w1 - w3) / 2), math.floor((h1 - h3) / 2)))
            self._image = new_image.resize(size, Image.ANTIALIAS)
            _upsize(self, size)
        else:
            w0, h0, w1, h1 = old_size + size
            if mode in ['repeat', 'repeat-x', 'repeat-y', 'round', 'round-x', 'round-y']:
                if mode in ['round', 'round-x', 'round-y']:
                    w0, h0 = math.floor(w1 / 2 if w1 / 1.5 >= w0 else w0), math.floor(h1 / 2 if h1 / 1.5 >= h0 else h0)
                    xl, yl = math.floor(w1 / w0), math.floor(h1 / h0)
                    w0, h0 = min(w0 + round((w1 - (w0 * xl)) / xl), w1), min(h0 + round((h1 - (h0 * yl)) / yl), h1)
                    old_image = old_image.resize((w0, h0), Image.ANTIALIAS)
                    new_image = Image.new('RGBA', (w0 * xl, h0 * yl))
                else:
                    xl, yl = round(w1 / w0) + 1, round(h1 / h0) + 1
                    new_image = Image.new('RGBA', size)
                for x in range(xl):
                    if mode in ['repeat-x', 'round-x']:
                        new_image.paste(old_image, (round(w0 * x), 0))
                    else:
                        for y in range(yl): new_image.paste(old_image, (round(w0 * x), round(h0 * y)))
                        if mode in ['repeat-y', 'round-y']: break
                if mode in ['round', 'round-x', 'round-y']: self._image = new_image.resize(size, Image.ANTIALIAS)
                else: self._image = new_image
                _upsize(self, size)
            elif size + (x, y) != old_size + (0, 0):
                new_image = Image.new('RGBA', size)
                new_image.paste(old_image, (x, y))
                self._image = new_image
                _upsize(self, size)
        return self

    def linear_gradient(self, values, position='bottom'):
        if isinstance(values, tuple) and len(values) >= 2:
            old_image, new_image = self._image.copy(), Image.new('RGBA', self.size)
            colors, newdata, positions = [], [], ['bottom', 'top', 'left', 'right']
            (width, height), isx, count = old_image.size, position in positions[2 : 4], len(values)
            length, items = width if isx else height, count - 1
            for i in range(count):
                try:
                    color, percentage = values[i]
                    if isx:
                        w = round((width / 100) * min(max(percentage, 1), 100))
                        more = round((width - w) / count)
                        value = (w + more, height), more, color
                        width -= w + more
                        length -= w + more
                    else:
                        h = round((height / 100) * min(max(percentage, 1), 100))
                        more = round((height - h) / count)
                        value = (width, h + more), more, color
                        height -= h + more
                        length -= h + more
                    items -= 1
                except:
                    color = values[i]
                    if i >= count - 2:
                        if isx: w, h, percentage = length, height, length
                        else: w, h, percentage = width, length, length
                    else:
                        if isx:
                            w, h = round(width / items), height
                            length -= w
                            percentage = w
                        else:
                            w, h = width, round(height / items)
                            length -= h
                            percentage = h
                    value = (w, h), percentage, color
                colors.append(value)
            for i in range(len(colors) - 1):
                ((w, h), percentage, color), mix = colors[i : i + 2]
                color, less, mix, value = Color.new(color), 100 / percentage, mix[2], 100
                if isx:
                    for x in range(w):
                        newdata.append(color.mix(mix, value / 100).rgba)
                        if x >= w - percentage: value -= less
                else:
                    for y in range(h):
                        newdata += [color.mix(mix, value / 100).rgba] * w
                        if y >= h - percentage: value -= less
            if isx: newdata = newdata * old_image.size[1]
            if position in positions[1 : 3]: newdata = list(reversed(newdata))
            new_image.putdata(newdata)
            new_image = Image.alpha_composite(old_image, new_image)
            try: self._image.paste(new_image, (0, 0), self._corners[0])
            except: self._image = new_image
        return self

    def shadow_inside(self, x, y, blur, solid, color, *argsv):
        if x > 0 or y > 0 or blur > 0:
            (w, h), color = self._image.size, Color.new(color)
            weight = round(blur + solid)
            shadow = Image.new('RGBA', (w + (weight * 2), h + (weight * 2)), color)
            rectsize = round((w - (solid * 2))), round((h - (solid * 2)))
            rectx = x + ((shadow.size[0] - rectsize[0]) / 2)
            recty = y + ((shadow.size[1] - rectsize[1]) / 2)
            rect = Image.new('RGBA', rectsize, color.alpha(0).rgba)
            if self._corners: shadow.paste(rect, (round(rectx), round(recty)), _newcorners(self, rectsize)[0])
            else: shadow.paste(rect, (round(rectx), round(recty)))
            if blur > 0:
                blur = round((255 if blur > 255 else blur) / 3.5)
                shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
            new_image = Image.new('RGBA', (w, h))
            new_image.paste(shadow, (-weight, -weight))
            new_image = Image.alpha_composite(self._image, new_image)
            if self._corners:
                corners = Image.new('RGBA', (w, h))
                corners.paste(new_image, (0, 0), self._corners[0])
                new_image = corners
            self._image = new_image
        return self

    # border
    def border(self, values, color='transparent', style='solid', image=None):
        corners = getcorners(values)
        if corners != (0, 0, 0, 0):
            old_image, old_size = self._image, self._image.size
            (w0, h0), (t, r, b, l) = old_size, corners
            new_size = old_size[0] + r + l, old_size[1] + t + b
            (w1, h1), color = new_size, Color.new(color)
            # by style
            if style in ['inbutton', 'outbutton', 'inset', 'outset']:
                big_size = math.floor(w1 * 2), math.floor(h1 * 2)
                (w1, h1), t1, r1, b1, l1 = big_size, math.floor(t * 2), math.floor(r * 2), math.floor(b * 2), math.floor(l * 2)
                new_border = Image.new('RGBA', big_size, color.rgba)
                draw = ImageDraw.Draw(new_border)
                color = 'white' if style in ['inbutton', 'outbutton'] else color.light(0.5).rgba
                if style in ['inbutton', 'inset']: draw.polygon([(0, 0), (w1 - 1, 0), (w1 - r1, t1), (l1, h1 - b1), (0, h1 - 1)], color)
                elif style in ['outbutton', 'outset']: draw.polygon([(w1, h1), (w1 - 1, 0), (w1 - r1, t1), (l1, h1 - b1), (0, h1 - 1)], color)
                new_image = new_border.resize(new_size, Image.ANTIALIAS)
            else:
                new_image = Image.new('RGBA', new_size, color.rgba)
                # by image
                if image:
                    image = image._image.convert('RGBA').resize(new_size, Image.ANTIALIAS)
                    new_image = Image.alpha_composite(new_image, image)
            # new image
            if self._corners: new_image.paste(old_image, (l, t), self._corners[0])
            else: new_image.paste(old_image, (l, t))
            self._border = corners
            self._image = new_image
            self._position[0] += l
            self._position[1] += t
            _upcorners(self, new_size)
            # devolve
        return self

    def corners(self, *values):
        corners = getcorners(values)
        if corners == (0, 0, 0, 0):
            self._corners = None
        else:
            old_size = self._image.size
            self._corners = _cornersmask(old_size, corners, False)
            _cropcorners(self, old_size)
        return self

    def shadow_outside(self, x, y, blur, solid, color, inset=False):
        if x > 0 or y > 0 or blur > 0 or solid > 0:
            (w, h), color = self._image.size, Color.new(color)
            weight = blur + solid
            width, height, = w + (weight * 2), h + (weight * 2)
            morex = abs(x) - weight if abs(x) >= weight else 0
            morey = abs(y) - weight if abs(y) >= weight else 0
            shadow = Image.new('RGBA', (round(width + morex), round(height + morey)), color.alpha(0).rgba)
            rectsize = w + (solid * 2), h + (solid * 2)
            rectx = shadow.size[0] - (rectsize[0] + blur) if x > -1 else blur
            recty = shadow.size[1] - (rectsize[1] + blur) if y > -1 else blur
            rect = Image.new('RGBA', rectsize, color)
            if self._corners: shadow.paste(rect, (round(rectx), round(recty)), _newcorners(self, rectsize)[0])
            else: shadow.paste(rect, (round(rectx), round(recty)))
            if blur > 0:
                blur = round((255 if blur > 255 else blur) / 2)
                shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
            centerx = round((shadow.size[0] - w) / 2)
            centery = round((shadow.size[1] - h) / 2)
            if -centerx >= x: x = centery * 2
            else: x = 0 if x >= centerx else centerx
            if -centery >= y: y = centery * 2
            else: y = 0 if y >= centery else centery
            new_image = shadow
            if self._corners:
                new_image.paste(self._image, (x, y), self._corners[0])
                self._corners = _newcorners(self, shadow.size)
            else:
                new_image.paste(self._image, (x, y))
            self._shadow = (abs(x), abs(y))
            self._position[0] += abs(x)
            self._position[1] += abs(y)
            self._image = new_image
        return self

    # filter
    def blur(self, value):
        value = getOne(value)
        if value != 0: self._image = self._image.filter(ImageFilter.GaussianBlur(math.floor(value * 10)))
        return self

    def brightness(self, value):
        value = getOne(value)
        if value != 0: self._image = ImageEnhance.Brightness(self._image).enhance(math.floor(value * 100))
        return self

    def opacity(self, value):
        value = getOne(value)
        if value != 1:
            newdata = []
            for item in self._image.getdata():
                r, g, b, a = item
                alpha = getNum(math.floor(value * a), 0, a)
                newdata.append((r, g, b, alpha))
        self._image.putdata(newdata)
        return self

    # resize
    def crop(self, w, h, x=0, y=0):
        if not self.size == (w, h) and self.size[0] >= w and self.size[1] >= h:
            self._image = self._image.crop((x, y, x + w, y + h))
            _upsize(self, self._image.size)
        return self

    def resize(self, *argsv, **argsk):
        image = self._image
        mode = argsk.get('mode', getItem(argsv, 1, 'fill'))
        width, height = image.size
        # get size
        new_width = getItem(argsk.get('size'), 0, argsk.get('width', getItem(argsv, (0, 0))))
        new_height = getItem(argsk.get('size'), 1, argsk.get('height', getItem(argsv, (0, 1))))
        # resize
        if new_width != None or new_height != None:
            # from fill
            if mode == 'fill' and new_width != None and new_height != None:
                size = math.floor(new_width), math.floor(new_height)
                if (width, height) != size:
                    self._image = image.resize(size, Image.ANTIALIAS)
                    _upsize(self, self._image.size)
            else:
                # real size
                real_width = new_height if new_width == None else new_width
                real_height = new_width if new_height == None else new_height
                # from height
                if (real_width > real_height) if mode == 'contain' else ((width > height and new_height != None) or new_width == None):
                    h = real_height if mode == 'contain' else new_height
                    w = width * (h / height)
                    if mode != 'contain' and new_width == None:
                        new_width = w
                    elif mode != 'contain' and new_width > w:
                        w = new_width;
                        h = height * (w / width)
                # from width
                else:
                    w = real_width if mode == 'contain' else new_width
                    h = height * (w / width)
                    if mode != 'contain' and new_height == None:
                        new_height = h
                    elif mode != 'contain' and new_height > h:
                        h = new_height
                        w = width * (h / height)
                # new image
                if mode in ['contain', 'cover']:
                    # position
                    x = round(-((w - real_width) / 2) if w > real_width else (real_width - w) / 2)
                    y = round(-((h - real_height) / 2) if h > real_height else (real_height - h) / 2)
                    # create
                    self._image = Image.new('RGBA', (round(real_width), round(real_height)))
                    self._image.paste(image.resize((round(w), round(h)), Image.ANTIALIAS), (round(x), round(y)))
                else:
                    # create
                    self._image = image.resize((round(w), round(h)), Image.ANTIALIAS)
                _upsize(self, self._image.size)
        return self

    def rotate(self, rotate):
        try:
            self._image = self._image.rotate(rotate)
            _upsize(self, self._image.size)
        except:
            pass
        return self

    # main
    def tkinter(self):
        return ImageTk.PhotoImage(self._image)

    def copy(self):
        image = img(self._image.copy(), self._color.rgba)
        image._size, image._padding,  = self._size,  self._padding
        image._border, image._corners =  self._border, self._corners
        image._position, image._shadow = self._position, self._shadow
        return image

    def save(self, *argsv, **argsk):
        self._image.save(*argsv, **argsk)

    def show(self):
         self._image.show()

    @property
    def size(self):
        return self._image.size

    @property
    def realsize(self):
        w, h =  self._size
        bt, br, bb, bl = self._border
        pt, pr, pb, pl = self._padding
        return w + br + bl + pr + pl, h + bt + bb + pt + pb

    def __init__(self, image, color):
        self._image, self._size = image,  image.size
        self._corners, self._color = None, Color.new(color)
        self._border, self._padding = (0, 0, 0, 0), (0, 0, 0, 0)
        self._position, self._shadow = [0, 0], (0, 0)

def draw(image):
    return ImageDraw.Draw(image._image)

def new(size, color='transparent'):
    return img(Image.new('RGBA', size, Color.new(color).rgba), color)

# open file
def open(path):
    if isinstance(path, bytes):
        return img(Image.open(io.BytesIO(path)).convert('RGBA'), 'transparent')
    else:
        return img(Image.open(path).convert('RGBA'), 'transparent')

# end
setModule(__name__, '__call__', new)
