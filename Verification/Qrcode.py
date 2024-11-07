import cv2


# A class to handle QR code reading and processing using OpenCV.
# Methods:
# --------
# __init__() -> None
#     Initializes the Qrcode class.
# read(filename: str = None) -> str
#     Reads a QR code from the given image file and returns the decoded data as a string.
# invert_image(image: str) -> str
#     Inverts the colors of the given image and returns the inverted image.

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