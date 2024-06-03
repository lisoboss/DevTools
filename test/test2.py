import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(["Files"])
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.initUI()
    
    def initUI(self):
        root = QTreeWidgetItem(self, ["Root"])
        root.setFlags(root.flags() | Qt.ItemIsEditable)  # 设置可编辑
        folder1 = QTreeWidgetItem(root, ["Folder1"])
        folder1.setFlags(folder1.flags() | Qt.ItemIsEditable)  # 设置可编辑
        folder2 = QTreeWidgetItem(root, ["Folder2"])
        folder2.setFlags(folder2.flags() | Qt.ItemIsEditable)  # 设置可编辑
        file1 = QTreeWidgetItem(folder1, ["File1"])
        file1.setFlags(file1.flags() | Qt.ItemIsEditable)  # 设置可编辑
        file2 = QTreeWidgetItem(folder1, ["File2"])
        file2.setFlags(file2.flags() | Qt.ItemIsEditable)  # 设置可编辑
        file3 = QTreeWidgetItem(folder2, ["File3"])
        file3.setFlags(file3.flags() | Qt.ItemIsEditable)  # 设置可编辑
        file4 = QTreeWidgetItem(folder2, ["File4"])
        file4.setFlags(file4.flags() | Qt.ItemIsEditable)  # 设置可编辑
        self.expandAll()
    
    def onItemDoubleClicked(self, item, column):
        self.editItem(item, column)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tree Structure Example")
        self.setGeometry(300, 300, 400, 300)
        self.treeWidget = TreeWidget()
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.treeWidget)
        
        self.container = QWidget()
        self.container.setLayout(self.layout)
        
        self.setCentralWidget(self.container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
