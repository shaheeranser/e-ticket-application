from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from qr_code import ScannerThread
from PySide6.QtCore import QTimer

class ScanTicket(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout(self)
        self.camera_label = QLabel("Camera Off")
        self.camera_label.setFixedSize(640, 480)
        self.layout.addWidget(self.camera_label)
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)
        self.thread = ScannerThread()
        self.thread.frame_signal.connect(self.update_image)
        self.thread.scanned_signal.connect(self.handle_scan)

    def start_camera(self):
        self.thread._running = True
        self.thread.start()

    def stop_camera(self):
        self.thread.stop()

    def update_image(self, q_image):
        self.camera_label.setPixmap(QPixmap.fromImage(q_image))

    def handle_scan(self, data):
        self.thread.stop()
        try:
            parts = data.split(",")
            sap_id = int(parts[0].split(":")[-1].strip())
            self.db.mark_checked_in(sap_id)
            self.show_status(f"Ticket {sap_id} checked in successfully!")
        except Exception as e:
            self.show_status(f"Error: {str(e)}")
        QTimer.singleShot(2000, lambda: self.start_camera())

    def show_status(self, message):
        self.status_label.clear()
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.clear())