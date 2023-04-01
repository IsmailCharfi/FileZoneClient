from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QFormLayout, \
    QMessageBox
from PyQt5.QtCore import Qt


class AuthWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.error_label = QLabel()
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap('logo.jpg').scaledToHeight(100))
        self.app_name_label = QLabel('File Zone')
        self.app_name_label.setStyleSheet('font-size: 36pt; font-weight: bold;')

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        # Create layout and add widgets to it
        layout = QVBoxLayout()

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.app_name_label)
        logo_layout.setAlignment(Qt.AlignHCenter)

        form_layout = QFormLayout()
        form_layout.addRow("Username: ", self.username_edit)
        form_layout.addRow("Password: ", self.password_edit)
        form_layout.addRow("", self.login_button)
        form_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(logo_layout)
        layout.addWidget(self.error_label)
        layout.addLayout(form_layout)

        self.setLayout(layout)

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        try:
            response = self.window().api.post("/login", data={"username": username, "password": password})

            if response.status_code == 200:
                self.error_label.setText("")
                self.window().show_main_widget()
            else:
                self.error_label.setText("Invalid username or password")
        except Exception as e:
            QMessageBox.warning(self, "Login Error", str(e))
