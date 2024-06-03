import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(["Tree"])
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.root = QTreeWidgetItem(self, ["Root"])
        self.expandAll()

    def addG(self, name):
        item = QTreeWidgetItem(self.root, [name, '{}'])
        print(item.text(1))
        return item

    def addI(self, name):
        item = QTreeWidgetItem(self.root, [name, '{}'])
        item.setFlags(item.flags() | Qt.ItemIsEditable | Qt.ItemIsUserCheckable) # 设置可编辑
        item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled)
        print(item.text(1))
        return item

    def onItemDoubleClicked(self, item, column):
        self.editItem(item, column)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            selected_items = self.selectedItems()
            for item in selected_items:
                if item.text(0) != "Root":
                    parent = item.parent()
                    if parent:
                        parent.removeChild(item)     
        else:
            super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tree Structure Example")
        self.setGeometry(300, 300, 400, 300)

        treeWidget = TreeWidget()
        
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)

        b = QPushButton('GroupV')
        b.clicked.connect(lambda _: treeWidget.addG('GroupV'))
        l.addWidget(b)

        b = QPushButton('GroupH')
        b.clicked.connect(lambda _: treeWidget.addG('GroupH'))
        l.addWidget(b)

        b = QPushButton('Item')
        b.clicked.connect(lambda _: treeWidget.addI('Item'))
        l.addWidget(b)

        b = QPushButton('Item2')
        b.clicked.connect(lambda _: treeWidget.addI('Item2'))
        l.addWidget(b)

        b = QPushButton('Copy')
        b.clicked.connect(lambda _: self.copy(treeWidget))
        l.addWidget(b)

        w2 = QWidget()
        l = QHBoxLayout()
        w2.setLayout(l)

        l.addWidget(treeWidget, 2)

        layout = QVBoxLayout()
        w3 = QWidget()
        w3.setLayout(layout)
        l.addWidget(w3, 8)

        l = QVBoxLayout()
        l.addWidget(w, 1)
        l.addWidget(w2, 30)

        layout.addWidget(QPushButton('1111'))
        
        # Hlayout = QHBoxLayout()
        # Hlayout.addWidget(self.treeWidget)
        # Hlayout.addWidget(self.treeWidget)
        # Vlayout = QVBoxLayout()
        # self.layout.addWidget(TreeWidget())
        # self.layout.addWidget(self.treeWidget)
        
        
        container = QWidget() 
        container.setLayout(l)
        
        self.setCentralWidget(container)

    def copy(self, treeWidget):
        # l = QTreeWidgetItem.childCount()
        n = treeWidget.root.childCount()
        print(n)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())