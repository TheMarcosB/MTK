import _lib
from lib import MTK
w = MTK.window()
w.document.title.value = 'Test'
body = w.document.body
entry = body.createTag('entry')
entry.style({
   'width': '100px',
   'height': '16px',
   'line-height': '16px',
   'padding': ('5px', '10px'),
   'border': ('1px', 'solid', 'black'),
   'border-radius': '2px'
})
check = body.createTag('check')
radio = body.createTag('radio')
switch = body.createTag('switch')
select = body.createTag('select')
select.createItem('marcos', 'test', 'thiago', 'ana')
MTK.loop()
