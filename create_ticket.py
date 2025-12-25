from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit, QWidget, QVBoxLayout
from PySide6.QtGui import QTextDocument, QPageSize, QPdfWriter
from PySide6.QtCore import QTimer, QSizeF
from qr_code import generate_qr
import os

class CreateTicket(QWidget):
    def __init__(self, db, ticket_dir, template_path):
        super().__init__()
        self.setWindowTitle("Create Ticket")
        self.db = db
        self.ticket_dir = ticket_dir
        self.template_path = template_path
        self.layout = QVBoxLayout()
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)
        self.sap_id_input = QLineEdit(self)
        self.sap_id_input.setPlaceholderText("Enter SAP ID")
        self.layout.addWidget(self.sap_id_input)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Name")
        self.layout.addWidget(self.name_input)
        self.create_button = QPushButton("Create Ticket", self)
        self.create_button.clicked.connect(self.create_ticket)
        self.create_button.clicked.connect(self.generate_ticket_pdf)
        self.layout.addWidget(self.create_button)
        self.setLayout(self.layout)

    def generate_ticket_pdf(self):
        sap_id = int(self.sap_id_input.text())
        name = self.name_input.text()
        pdf_path = self.ticket_dir / f"ticket_{sap_id}.pdf"
        qr_path = self.ticket_dir / f"qr_{sap_id}.png"
        generate_qr(f"SAP ID: {sap_id}, Name: {name}", str(qr_path))
        template = self.template_path.read_text()
        ticket_html = template.replace("{{ sap_id }}", str(sap_id)) \
                                    .replace("{{ name }}", name) \
                                    .replace("{{ qr_path }}", qr_path.absolute().as_uri())
        pdf_writer = QPdfWriter(str(pdf_path))
        mobile_size = QSizeF(100, 200)
        custom_page_size = QPageSize(mobile_size, QPageSize.Millimeter)
        pdf_writer.setPageSize(custom_page_size)
        pdf_writer.setResolution(300)
        document = QTextDocument()
        document.setPageSize(pdf_writer.pageLayout().paintRectPixels(300).size())
        document.setHtml(ticket_html)
        document.print_(pdf_writer)
        if qr_path.exists():
            os.remove(qr_path)
        return pdf_path

    def create_ticket(self):
        sap_id = int(self.sap_id_input.text())
        name = self.name_input.text()
        try:
            self.db.create_ticket(sap_id, name)
            self.show_status(f"Ticket {sap_id} created successfully!")
        except Exception as e:
            self.show_status(f"Error: {str(e)}")
    
    def show_status(self, message):
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.clear())
