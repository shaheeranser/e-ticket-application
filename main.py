from PySide6.QtWidgets import *
from database import Database
from qr_code import *

app = QApplication([])
db = Database()

window = QMainWindow()

window.setWindowTitle("Hello World")
window.setGeometry(100, 100, 600, 400)

label = QLabel("Hello, World!", parent=window)
label.show()

# add_button = QPushButton("Add Data", parent=window)
# add_button.clicked.connect(lambda: db.create_ticket(69420, 'Freak Bob'))
# add_button.show()

# check_in_button = QPushButton("Check In", parent=window)
# check_in_button.clicked.connect(lambda: db.mark_checked_in(69420))
# check_in_button.show()

# delete_button = QPushButton("Delete Data", parent=window)
# delete_button.clicked.connect(lambda: db.delete_ticket(69420))
# delete_button.show()

layout = QVBoxLayout()
layout.addWidget(label)
# layout.addWidget(add_button)
# layout.addWidget(check_in_button)
# layout.addWidget(delete_button)
# central_widget = QWidget()
# central_widget.setLayout(layout)
# window.setCentralWidget(central_widget)

# window = MainWindow()
window.show()

app.exec()