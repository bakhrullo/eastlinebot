from pyzbar.pyzbar import decode
from PIL import Image
# import sys, qrcode
# from qrcode import QRCode

# import qrtools
# from qrtools import QR
# import cv2
# Name of the QR Code Image file
# qr = qrtools.QR()
# qr.decode("qr/test.jpg")
# print(qr.data)


#
#
# d = qrcode.()
# if d.decode('qr/test.jpg'):
#     print('result: ' + d.result)
# else:
#     print('error: ' + d.error)
#
#

# def decoderv2():
#     filename = "qr/test.jpg"
#     # read the QRCODE image
#     image = cv2.imread(filename)
#     # initialize the cv2 QRCode detector
#     detector = cv2.QRCodeDetector()
#     # detect and decode
#     data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
#     # if there is a QR code
#     # print the data
#     if vertices_array is not None:
#         print("QRCode data:")
#         print(data)
#         return data
#     else:
#         error = 'отправьте более четкое фото'
#         return error

def decoder():
     try:
         decocdeQR = decode(Image.open('qr/test.jpg'))
         print(decocdeQR[0].data.decode('ascii'))
         code = decocdeQR[0].data.decode('ascii')
         return code

     except:
         word = 'отправьте более четкое фото'
         return word