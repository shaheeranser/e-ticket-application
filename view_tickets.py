from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QPushButton, QLabel
from PySide6.QtCore import QTimer

class ViewTickets(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        layout = QVBoxLayout(self)
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        self.table = QTableView()
        self.table.setModel(self.db.model)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.refresh_data)
        layout.addWidget(self.table)
        layout.addWidget(self.refresh_btn)
        self.refresh_data()

    def refresh_data(self):
        self.db.model.select()
        self.add_delete_buttons()

    def add_delete_buttons(self):
        for row in range(self.db.model.rowCount()):
            index = self.db.model.index(row, 0)
            sap_id = self.db.model.data(index)
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("background-color: #ff4d4d; color: white;")
            delete_button.clicked.connect(lambda checked=False, sap_id=sap_id: self.confirm_delete(sap_id))
            self.table.setIndexWidget(self.db.model.index(row, 3), delete_button)

    def confirm_delete(self, sap_id):
        self.db.delete_ticket(sap_id)
        self.show_status("Tickets Deleted Successfully")
        self.refresh_data()
    
    def show_status(self, message):
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.clear())