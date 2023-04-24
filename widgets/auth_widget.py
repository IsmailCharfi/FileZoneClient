from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QFormLayout, \
    QMessageBox
from PyQt5.QtCore import Qt

from model import User


class AuthWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.error_label = QLabel()
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap('logo.jpg').scaledToHeight(180))
        self.app_name_label = QLabel('File Zone')
        self.app_name_label.setStyleSheet('font-size: 60pt; font-weight: bold;')

        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Login')
        self.sign_up_button = QPushButton('Sign up')
        self.login_button.clicked.connect(self.login)
        self.sign_up_button.clicked.connect(self.window().show_sign_up_widget)

        # Create layout and add widgets to it
        layout = QVBoxLayout()

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.app_name_label)
        logo_layout.setAlignment(Qt.AlignHCenter)
        logo_layout.setContentsMargins(1, 100, 1, 1)

        form_layout = QFormLayout()
        form_layout.addRow("Email: ", self.email_edit)
        form_layout.addRow("Password: ", self.password_edit)
        form_layout.addRow("", self.login_button)
        form_layout.addRow("", self.sign_up_button)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setContentsMargins(1, 1, 1, 150)

        layout.addLayout(logo_layout)
        layout.addWidget(self.error_label)
        layout.addLayout(form_layout)

        self.setLayout(layout)

    def login(self):
        email = self.email_edit.text()
        password = self.password_edit.text()
        try:
            response = self.window().api.post("/login", data={"email": email, "password": password}, use_kerberos=False)
            if response.status_code == 500:
                QMessageBox.critical(self, "Login Failure", "an error has occurred")
            elif response.status_code == 200:
                self.email_edit.setText("")
                self.password_edit.setText("")
                self.error_label.setText("")
                self.window().user = User(response.json().get("user"))
                self.window().show_main_widget()
            else:
                self.error_label.setText("Invalid username or password")
        except Exception as e:
            QMessageBox.critical(self, "Login Failure", str(e))
