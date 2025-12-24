import segno
import cv2
from PySide6.QtCore import *

def generate_qr(data, filename):
    qrcode = segno.make_qr(data)
    qrcode.save(filename, scale=10)

class ScannerThread(QThread):
    scanned_signal = Signal(str)

    def run(self):
        cap = cv2.VideoCapture(0)
        detector = cv2.wechat_qrcode_WeChatQRCode()

        while not self.isInterruptionRequested():
            ret, frame = cap.read()
            if ret:
                data, points = detector.detectAndDecode(frame)
                if data:
                    self.scanned_signal.emit(data[0])
        
        cap.release()