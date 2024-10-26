from .Qrcode import Qrcode

class Verification():
    def __init__(self):
        pass
    
    def verify(self, image):
        Qr = Qrcode(image)
        Qr_data = Qr.read()
        if Qr_data:
            pass