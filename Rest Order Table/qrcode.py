import pyqrcode
import png

email = "AbhishekGupta@xyz.com"
mob = '1234567890'
myqrcode = pyqrcode.create('Email : '+email+'\nMobile No : '+mob)
myqrcode.png('QrCode.png')
print('Done..')
