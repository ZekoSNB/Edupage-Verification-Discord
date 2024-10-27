import cv2

class Qrcode():
    def __init__(self):
        pass        
    
    def read(self, filename:str=None) -> str:
        try:
            if filename is None:
                return None
            image = cv2.imread(filename)
            detector = cv2.QRCodeDetector()
            data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
            
            if not data:
                inverted_image = self.invert_image(image)
                data, vertices_array, binary_qrcode = detector.detectAndDecode(inverted_image) 

            if vertices_array is not None:
                return data
            return None
        except Exception as e:
            return None
    
    def invert_image(self, image:str) -> str:
        return cv2.bitwise_not(image)