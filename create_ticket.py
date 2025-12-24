from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit, QWidget, QVBoxLayout
from PySide6.QtGui import QTextDocument, QPageSize, QImage, QPdfWriter
from qr_code import generate_qr
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TICKET_DIR = BASE_DIR / "generated_tickets"
TICKET_DIR.mkdir(exist_ok=True)

class CreateTicket(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Create Ticket")
        self.db = db
        self.layout = QVBoxLayout()
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
        pdf_path = TICKET_DIR / f"ticket_{sap_id}.pdf"
        qr_path = TICKET_DIR / f"qr_{sap_id}.png"
        generate_qr(f"SAP ID: {sap_id}, Name: {name}", str(qr_path))
        template_path = BASE_DIR / "template.html"
        template = template_path.read_text()
        ticket_html = template.replace("{{ sap_id }}", str(sap_id)) \
                                    .replace("{{ name }}", name) \
                                    .replace("{{ qr_path }}", qr_path.absolute().as_uri())
        pdf_writer = QPdfWriter(str(pdf_path))
        pdf_writer.setPageSize(QPageSize(QPageSize.A6))
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
            QLabel("Ticket created successfully!", parent=self).show()
        except Exception as e:
            QLabel(f"Error: {str(e)}", parent=self).show()
