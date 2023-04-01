from PyQt5.QtCore import Qt, QDir, QFile, QIODevice, QDataStream
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QFileDialog, QAction, QMenu, \
    QInputDialog, QLineEdit


class File:
    def __init__(self, name, parent_folder=None, is_folder=False):
        self.name = name
        self.parent_folder = parent_folder
        self.is_folder = is_folder
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

    def get_path(self):
        if self.parent_folder is None:
            return self.name
        else:
            return f"{self.parent_folder.get_path()}/{self.name}"


class FileSystemModel(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.model = self.create_model()
        self.setModel(self.model)
        self.doubleClicked.connect(self.open_file)

    def create_model(self):
        root_node = File("root", is_folder=True)
        model = QFileSystemModel()
        model.setRootPath(QDir.rootPath())
        model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        model.setReadOnly(False)
        model.setRootPath(root_node.get_path())
        return model

    def create_file(self, name, is_folder=False):
        selected = self.selectionModel().selectedIndexes()
        if not selected:
            return
        parent_index = selected[0]
        parent_node = self.model.itemFromIndex(parent_index)
        if not parent_node.is_folder:
            return
        parent_path = parent_node.get_path()
        new_file = File(name, parent_node, is_folder)
        parent_node.add_child(new_file)
        index = self.model.indexFromItem(new_file, parent_index)
        self.model.layoutChanged.emit()
        self.scrollTo(index)

    def create_file_dialog(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Create file")
        if not file_name:
            return
        self.create_file(file_name)

    def create_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Create folder", "Folder name:", QLineEdit.Normal, "")
        if not ok or not folder_name:
            return
        self.create_file(folder_name, is_folder=True)

    def context_menu(self, pos):
        selected = self.selectionModel().selectedIndexes()
        if len(selected) > 0:
            node = self.model.itemFromIndex(selected[0])
            menu = QMenu()
            create_folder_action = QAction(QIcon(), "Create folder", self)
            create_folder_action.triggered.connect(self.create_folder)
            create_file_action = QAction(QIcon(), "Create file", self)
            create_file_action.triggered.connect(self.create_file_dialog)
            download_action = QAction(QIcon(), "Download", self)
            download_action.triggered.connect(self.download)
            refresh_action = QAction(QIcon(), "Refresh", self)
            refresh_action.triggered.connect(self.refresh)

            if node.is_folder:
                menu.addAction(create_folder_action)
                menu.addAction(create_file_action)
            else:
                menu.addAction(download_action)

            menu.addAction(refresh_action)
            menu.exec_(self.viewport().mapToGlobal(pos))

    def open_file(self, index):
        file_node = self.model.itemFromIndex(index)
        if not file_node.is_folder:
            file_path = file_node.get_path()
            file = QFile(file_path)
            if file.open(QIODevice.ReadOnly):
                stream = QDataStream(file)
                file_data = stream.readQString()
                file.close()
                print(file_data)

    def download(self):
        selected = self.selectionModel().selectedIndexes()
        if not selected:
            return
        file_node = self.model.itemFromIndex(selected[0])
        if file_node.is_folder:
            return
        file_path = file_node.get_path()
        save_file_path, _ = QFileDialog.getSaveFileName(self, "Save file", file_node.name)
        if not save_file_path:
            return
        QFile.copy(file_path, save_file_path)

    def refresh(self):
        selected = self.selectionModel().selectedIndexes()
        if len(selected) > 0:
            node = self.model.itemFromIndex(selected[0])
            parent = node.parent()
            row = node.row()
            self.model.layoutAboutToBeChanged.emit()
            self.model.removeRow(row, parent)
            self.model.insertRow(row, parent, node.file_data())
            self.model.layoutChanged.emit()
            self.setCurrentIndex(self.model.index(row, 0, parent))


from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My File Manager")
        self.setGeometry(100, 100, 800, 600)

        # Create the file system model
        self.file_system_model = FileSystemModel(self)

        # Set the model as the central widget
        self.setCentralWidget(self.file_system_model)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
