from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem
from model.storable import Storable, StorableType
from datetime import datetime

fs = []


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create layout
        main_layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # create buttons
        refresh_button = QPushButton("Refresh")
        download_button = QPushButton("Download")
        upload_button = QPushButton("Upload")
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(download_button)
        button_layout.addWidget(upload_button)

        file_tree = QTreeWidget()
        file_tree.setHeaderLabels(["Name", "Size", "Date Modified"])
        main_layout.addWidget(file_tree)

        # add sample files to the tree
        for item in fs:
            self.draw_node(item, file_tree)

    def draw_node(self, item: Storable, parent):
        node = QTreeWidgetItem(parent)
        if item.type == StorableType.DIRECTORY:
            node.setText(0, item.name)
            for child in item.children:
                self.drawNode(child, node)
            if len(item.children) == 0:
                empty_node = QTreeWidgetItem(node)
                empty_node.setText(0, "Empty")

        else:
            node.setText(0, item.name)
            node.setText(1, f"{item.size} o")
            node.setText(2, item.modified_at.strftime("%Y-%m-%d %H:%M:%S") if item.modified_at else "-")
