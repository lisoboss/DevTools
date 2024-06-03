import sys
from PyQt5.QtWidgets import QApplication, QTreeView, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class CustomStandardItem(QStandardItem):
    def __init__(self, text, item_type):
        super().__init__(text)
        self.item_type = item_type  # "A" 或 "G"
        
    def type(self):
        return self.item_type


class TreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QTreeView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        source_item = self.currentIndex()
        target_item = self.indexAt(event.pos())

        source_node = self.model().itemFromIndex(source_item)
        target_node = self.model().itemFromIndex(target_item)

        if target_node.item_type == "A":
            event.ignore()
        else:
            super().dropEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tree Structure with Drag and Drop")
        self.setGeometry(300, 100, 600, 400)

        layout = QVBoxLayout()
        self.tree_view = TreeView()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Items'])

        root_node = self.model.invisibleRootItem()

        # Example data
        g1 = CustomStandardItem("Group 1", "G")
        a1 = CustomStandardItem("Item A1", "A")
        g2 = CustomStandardItem("Group 2", "G")
        a2 = CustomStandardItem("Item A2", "A")
        g3 = CustomStandardItem("Group 3", "G")

        g1.appendRow(a1)
        g1.appendRow(g2)
        g2.appendRow(a2)
        root_node.appendRow(g1)
        root_node.appendRow(g3)

        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()

        layout.addWidget(self.tree_view)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
