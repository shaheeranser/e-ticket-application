from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout)
from database import Database
from create_ticket import CreateTicket
from scan_ticket import ScanTicket
from view_tickets import ViewTickets
import sys
import os
from pathlib import Path

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent / relative_path

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

TEMPLATE_PATH = get_resource_path("template.html")

USER_WORKSPACE = get_app_dir() 
TICKET_DIR = USER_WORKSPACE / "generated_tickets"
DB_PATH = USER_WORKSPACE / "app_database.db"

TICKET_DIR.mkdir(exist_ok=True)

app = QApplication([])
db = Database(str(DB_PATH))

window = QMainWindow()
window.setWindowTitle("E-Ticket Application")
window.resize(800, 600)

create_ticket_view = CreateTicket(db, TICKET_DIR, TEMPLATE_PATH)
scan_ticket_view = ScanTicket(db)
view_tickets_view = ViewTickets(db)

main_container = QWidget()
main_layout = QVBoxLayout(main_container)

nav_layout = QHBoxLayout()
create_ticket_button = QPushButton("Create Ticket")
scan_ticket_button = QPushButton("Scan Ticket")
view_tickets_button = QPushButton("View Tickets")

for btn in [create_ticket_button, scan_ticket_button, view_tickets_button]:
    btn.setFixedHeight(40)
    nav_layout.addWidget(btn)

main_layout.addLayout(nav_layout)

stack = QStackedWidget()
stack.addWidget(create_ticket_view)
stack.addWidget(scan_ticket_view)
stack.addWidget(view_tickets_view)
main_layout.addWidget(stack)

window.setCentralWidget(main_container)

def switch_to_scan():
    stack.setCurrentIndex(1)
    scan_ticket_view.start_camera()

def switch_to_create():
    scan_ticket_view.stop_camera()
    stack.setCurrentIndex(0)

def switch_to_view():
    scan_ticket_view.stop_camera()
    stack.setCurrentIndex(2)
    view_tickets_view.refresh_data()

scan_ticket_button.clicked.connect(switch_to_scan)
create_ticket_button.clicked.connect(switch_to_create)
view_tickets_button.clicked.connect(switch_to_view)

window.show()
sys.exit(app.exec())