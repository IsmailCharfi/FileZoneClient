import sys
import qdarkstyle

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon

from rest_api import RestApi
from widgets.auth_widget import AuthWidget
from widgets.main_widget import MainWidget

API_PATH = "http://127.0.0.1:5000"

class App(QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.api = RestApi(API_PATH)
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

    def show_main_widget(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def show_auth_widget(self):
        self.stacked_widget.setCurrentWidget(self.auth_widget)


if __name__ == "__main__":
    q_app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    q_app.setStyleSheet(qdarkstyle.load_stylesheet())
    q_app.exec_()
