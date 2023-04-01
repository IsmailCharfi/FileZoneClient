from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem
from model.storable import Storable, StorableType

fs = [
    Storable(_id=1,
             name="ROOT",
             _type=StorableType.DIRECTORY,
             children=[
                 Storable(_id=2,
                          name="Folder1",
                          _type=StorableType.DIRECTORY,
                          children=[]
                          ),
                 Storable(_id=3,
                          name="Folder1",
                          _type=StorableType.DIRECTORY,
                          children=[Storable(_id=5,
                                             name="File2",
                                             _type=StorableType.MULTI_MEDIA,
                                             children=[]
                                             )]
                          ),
                 Storable(_id=4,
                          name="File1",
                          _type=StorableType.TEXT,
                          children=[]
                          )
             ]
             ),
    Storable(_id=1,
             name="ROOT2",
             _type=StorableType.DIRECTORY,
             children=[
                 Storable(_id=2,
                          name="Folder1",
                          _type=StorableType.DIRECTORY,
                          children=[]
                          ),
                 Storable(_id=3,
                          name="Folder1",
                          _type=StorableType.DIRECTORY,
                          children=[Storable(_id=5,
                                             name="File2",
                                             _type=StorableType.MULTI_MEDIA,
                                             children=[]
                                             )]
                          ),
                 Storable(_id=4,
                          name="File1",
                          _type=StorableType.TEXT,
                          children=[]
                          )
             ]
             )
]


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
            self.drawNode(item, file_tree)

    def drawNode(self, item, parent):
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
            node.setText(1, f"{10} MB")
            node.setText(2, "2022-01-01")
