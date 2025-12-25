import segno
import cv2
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

def generate_qr(data, filename):
    qrcode = segno.make_qr(data)
    qrcode.save(filename, scale=10)

class ScannerThread(QThread):
    scanned_signal = Signal(str)
    frame_signal = Signal(QImage)

    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        detector = cv2.wechat_qrcode_WeChatQRCode()

        while self._running:
            ret, frame = cap.read()
            if not ret:
                break

            data, points = detector.detectAndDecode(frame)
            if data:
                self.scanned_signal.emit(data[0])

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.frame_signal.emit(qt_image.copy())

        cap.release()

    def stop(self):
        self._running = False
        self.wait()