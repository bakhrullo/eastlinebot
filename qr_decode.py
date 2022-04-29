from pyzbar.pyzbar import decode
from PIL import Image


def decoder():
    try:
        decocdeQR = decode(Image.open('qr/test.jpg'))
        print(decocdeQR[0].data.decode('ascii'))
        code = decocdeQR[0].data.decode('ascii')
        return code

    except:
        word = 'отправьте более четкое фото'
        return word