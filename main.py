from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# Importing database module
from database import Database

# importing views here
from create_ticket import CreateTicket

app = QApplication([])
db = Database()

window = QMainWindow()
window.setWindowTitle("E-Ticket Application")
window.resize(800, 600)

create_ticket_view = CreateTicket(db)
window.setCentralWidget(create_ticket_view)

window.show()
app.exec()
