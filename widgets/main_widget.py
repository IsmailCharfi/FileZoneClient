from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTreeView, QTreeWidget, QTreeWidgetItem, \
    QMessageBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QFileDialog
from model import Storable, StorableType


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create layout
        self.main_layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        self.selected_storable = None
        # create buttons
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh)
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download)
        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.upload)
        self.create_folder_button = QPushButton("Create Folder")
        self.create_folder_button.clicked.connect(self.create_folder)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete)
        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addWidget(self.download_button)
        self.button_layout.addWidget(self.upload_button)
        self.button_layout.addWidget(self.create_folder_button)
        self.button_layout.addWidget(self.delete_button)

        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["Name", "Size", "Date Modified"])
        self.file_tree.setColumnWidth(0, 300)
        self.file_tree.clicked.connect(self.on_item_clicked)
        self.main_layout.addWidget(self.file_tree)

    def refresh(self):
        response = self.window().api.get(f"/users/{self.window().user.id}/root")
        if response.status_code == 200:
            root = Storable(response.json())
            self.init_fs(root)
        else:
            QMessageBox.critical(self, "Failure", "an error has occurred")

    def create_folder(self):
        dialog = NameDialog()
        result = dialog.exec_()
        if result == QDialog.Accepted:
            name = dialog.get_name()
            response = self.window().api.post(f"/{self.selected_storable.id}/add-folder", data={"name": name})
            if response.status_code == 200:
                self.refresh()
            else:
                QMessageBox.critical(self, "Failure", "an error has occurred")

    def delete(self):
        response = self.window().api.delete(f"/{self.selected_storable.id}")
        if response.status_code == 200:
            self.refresh()
        else:
            QMessageBox.critical(self, "Failure", "an error has occurred")

    def download(self):
        response = self.window().api.get(f"/{self.selected_storable.id}/content")
        if response.status_code == 200:
            path, _ = QFileDialog.getSaveFileName(None, "Save File", self.selected_storable.name)
            if path:
                with open(path, 'wb') as f:
                    f.write(response.content)
        else:
            QMessageBox.critical(self, "Failure", "an error has occurred")

    def upload(self):
        path, _ = QFileDialog.getOpenFileName(None, "Select a file", "")
        if path:
            response = self.window().api.post(f"/{self.selected_storable.id}/add-file", files={'file':  open(path, 'rb')})
            if response.status_code == 200:
                self.refresh()
            else:
                QMessageBox.critical(self, "Failure", "an error has occurred")

    def showEvent(self, event):
        super().showEvent(event)
        if not self.window().user:
            self.window().show_auth_widget()
        else:
            self.init_fs(self.window().user.root)

    def on_item_clicked(self):
        self.selected_storable = self.file_tree.currentItem().item
        if self.selected_storable:
            if self.selected_storable.isDir():
                self.download_button.setDisabled(True)
                self.upload_button.setDisabled(False)
                self.create_folder_button.setDisabled(False)
                self.delete_button.setDisabled(False)
            else:
                self.download_button.setDisabled(False)
                self.upload_button.setDisabled(True)
                self.create_folder_button.setDisabled(True)
                self.delete_button.setDisabled(False)
        else:
            self.download_button.setDisabled(True)
            self.upload_button.setDisabled(True)
            self.create_folder_button.setDisabled(True)
            self.delete_button.setDisabled(True)

    def init_fs(self, root):
        self.file_tree.clear()
        self.draw_node(root, self.file_tree)

        self.file_tree.expandAll()
        self.selected_storable = self.window().user.root

    def draw_node(self, item: Storable, parent):
        node = CustomTreeItem(parent, item)
        if item.type == StorableType.DIRECTORY.value:
            for child in item.children:
                self.draw_node(child, node)
            if len(item.children) == 0:
                empty_node = CustomTreeItem(node)
                empty_node.setText(0, "Empty")

        node.setText(0, item.name)
        node.setText(1, f"{item.size} bytes")
        node.setText(2, item.modified_at if item.modified_at else "-")


class CustomTreeItem(QTreeWidgetItem):
    def __init__(self, parent, item=None):
        super().__init__(parent)
        self.item = item


class NameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QFormLayout(self)
        self.name_input = QLineEdit(self)
        layout.addRow("Name:", self.name_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_name(self):
        return self.name_input.text()
