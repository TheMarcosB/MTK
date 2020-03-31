import _lib
from lib import MTK
w = MTK.window()
w.document.title.value = 'Select'
body = w.document.body
for i in range(4):
    select = body.createTag('select')
    select.createItem('marcos', 'test', 'thiago', 'ana')
    select.style.position = 'absolute'
    if i in [0, 1]: select.style.top = 0
    else: select.style.bottom = 0
    if i in [0, 3]: select.style.left = 0
    else: select.style.right = 0
    select.style.setHover(color='red')
MTK.loop()
