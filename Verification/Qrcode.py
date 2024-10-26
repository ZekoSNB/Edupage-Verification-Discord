import cv2

class Qrcode():
    def __init__(self, filename):
        self.filename = filename
        self.image = cv2.imread(filename)
    
    def read(self):
        detector = cv2.QRCodeDetector()
        data, vertices_array, binary_qrcode = detector.detectAndDecode(self.image)
        if vertices_array is not None:
            return data
        else:
            return None