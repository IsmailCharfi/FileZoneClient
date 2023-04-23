import os
import sys
import qdarkstyle

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon

from rest_api import RestApi
from widgets.auth_widget import AuthWidget
from widgets.main_widget import MainWidget
from widgets.sign_up_widget import SignUpWidget

API_PATH = "https://filezone.com:5000"

os.environ['REQUESTS_CA_BUNDLE'] = './certificate.crt'


class App(QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.api = RestApi(API_PATH)
        self.user = None
        self.setWindowTitle("File Zone")
        self.setWindowIcon(QIcon('logo.jpg'))
        self.setFixedSize(800, 600)
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.auth_widget = AuthWidget(self)
        self.stacked_widget.addWidget(self.auth_widget)
        self.main_widget = MainWidget(self)
        self.stacked_widget.addWidget(self.main_widget)
        self.sign_up_widget = SignUpWidget(self)
        self.stacked_widget.addWidget(self.sign_up_widget)

    def show_main_widget(self):
        if not self.user:
            self.show_auth_widget()
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def show_auth_widget(self):
        self.stacked_widget.setCurrentWidget(self.auth_widget)

    def show_sign_up_widget(self):
        self.stacked_widget.setCurrentWidget(self.sign_up_widget)


if __name__ == "__main__":
    q_app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    q_app.setStyleSheet(qdarkstyle.load_stylesheet())
    q_app.exec_()
