import sys
import json
import time
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


class B:
    name = ''
    value = {}

    def setFlags(self):
        self.item.setFlags(self.item.flags() | Qt.ItemIsEditable)  # 设置可编辑
        # self.item.setFlags(self.item.flags() | Qt.ItemIsEditable | Qt.ItemIsUserCheckable) # 设置可编辑
        self.item.setFlags(self.item.flags() | Qt.ItemIsUserCheckable)
        self.item.setFlags(self.item.flags() & ~Qt.ItemIsDropEnabled)

    def __init__(self, parent) -> None:
        self.item = QTreeWidgetItem(parent, [self.name, self.name, json.dumps(self.value)])
        self.setFlags()

    @staticmethod
    def edit(parent, value, update):
        for k, v in value.items():
            w, e = A(k, v)
            parent.addWidget(w)
            e.textChanged.connect((lambda k, update: lambda x: update(k, x))(k, update))


class Group(B):
    name = 'Group'
    value = {
        'layout': 'H',
        'weight': '1',
    }

    def setFlags(self):
        self.item.setFlags(self.item.flags() | Qt.ItemIsEditable)  # 设置可编辑

    @staticmethod
    def add(parent, value):
        w = QWidget()
        weight = int(value['weight'])
        parent.addWidget(w, weight)

        layout = value['layout']
        if layout == 'H':
            l = QHBoxLayout()
        elif layout == 'V':
            l = QVBoxLayout()
        else:
            l = QHBoxLayout()

        w.setLayout(l)

        return l

    @staticmethod
    def A(t, p, text, value):
        weight = value['weight']

        tt = f'w{t}_{TTT()}'
        ttt = f'l{t}_{TTT()}'

        l = value['layout']
        text += f'{tt} = QWidget()\n'
        text += f'{ttt} = Q{l}BoxLayout()\n'
        text += f'{tt}.setLayout({ttt})\n'
        text += f'{p}.addWidget({tt}, {weight})\n\n'

        return ttt, text


class Item_QLabel(B):
    name = 'QLabel'
    value = {
        'name': 'QLabel',
        'weight': '1',
    }

    @staticmethod
    def add(parent, value):
        parent.addWidget(QLabel(value['name']), int(value['weight']))

    @staticmethod
    def A(t, p, text, value):
        name = value['name']
        weight = value['weight']

        tt = f'qLabel{t}_{TTT()}'

        text += f'# {name}\n'
        text += f'{tt} = QLabel({name})\n'
        text += f'{p}.addWidget({tt}, {weight})\n\n'

        return text


class Item_QLineEdit(B):
    name = 'QLineEdit'
    value = {
        'name': 'QLineEdit',
        'weight': '1',
    }

    @staticmethod
    def add(parent, value):
        parent.addWidget(QLineEdit(), int(value['weight']))

    @staticmethod
    def A(t, p, text, value):
        name = value['name']
        weight = value['weight']

        tt = f'qLineEdit{t}_{TTT()}'

        text += f'# {name}\n'
        text += f'{tt} = QLineEdit()\n'
        text += f'{p}.addWidget({tt}, {weight})\n\n'

        return text


class Item_QTextEdit(B):
    name = 'QTextEdit'
    value = {
        'name': 'QTextEdit',
        'weight': '3',
    }

    @staticmethod
    def add(parent, value):
        parent.addWidget(QTextEdit(), int(value['weight']))

    @staticmethod
    def A(t, p, text, value):
        name = value['name']
        weight = value['weight']

        tt = f'qTextEdit{t}_{TTT()}'

        text += f'# {name}\n'
        text += f'{tt} = QTextEdit()\n'
        text += f'{p}.addWidget({tt}, {weight})\n\n'

        return text


class Item_QPushButton(B):
    name = 'QPushButton'
    value = {
        'name': 'QPushButton',
        'weight': '1',
    }

    @staticmethod
    def add(parent, value):
        parent.addWidget(QPushButton(value['name']), int(value['weight']))

    @staticmethod
    def A(t, p, text, value):
        name = value['name']
        weight = value['weight']

        tt = f'qPushButton{t}_{TTT()}'

        text += f'# {name}\n'
        text += f'{tt} = QPushButton({name})\n'
        text += f'{tt}.clicked.connect(lambda _: print("{tt}:", "未实现"))\n'
        text += f'{p}.addWidget({tt}, {weight})\n\n'

        return text


class Item_QComboBox(B):
    name = 'QComboBox'
    value = {
        'name': 'QComboBox',
        'weight': '1',
        'option': 'Option1,Option2,Option3'
    }

    @staticmethod
    def add(parent, value):
        q = QComboBox()
        for o in value['option'].split(","):
            q.addItem(o)
        parent.addWidget(q, int(value['weight']))

    @staticmethod
    def A(t, p, text, value):
        name = value['name']
        weight = value['weight']
        option = value['option']

        tt = f'qComboBox{t}_{TTT()}'

        text += f'# {name}\n'
        text += f'{tt} = QComboBox()\n'
        for o in value['option'].split(","):
            text += f'{tt}.addItem("{o}")\n'
        text += f'{tt}.currentIndexChanged.connect(lambda _: print("{tt}:", {tt}.currentText()))\n'
        text += f'{p}.addWidget({tt}, {weight})\n\n'

        return text


def A(name, value):
    w = QWidget()
    l = QHBoxLayout()
    w.setLayout(l)

    l.addWidget(QLabel(f'{name}: '), 1)
    e = QLineEdit(value)
    l.addWidget(e, 9)
    return w, e


def TTT():
    return str(int(time.time() * 100000000))[-6:]


K = {
    'QLabel': Item_QLabel,
    'QLineEdit': Item_QLineEdit,
    'QTextEdit': Item_QTextEdit,
    'QPushButton': Item_QPushButton,
    'QComboBox': Item_QComboBox,
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UITool")
        self.setGeometry(300, 300, 400, 300)

        self.tree = TreeWidget()
        self.tree.itemSelectionChanged.connect(self.item_selected)
        root = self.tree.root

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)

        w1 = QWidget()
        l1 = QHBoxLayout()
        w1.setLayout(l1)

        b = QPushButton('Group')
        b.clicked.connect(lambda _: Group(root))
        l1.addWidget(b)

        for Item in K.values():
            def C(Item):
                b = QPushButton(Item.name)
                b.clicked.connect(lambda _: Item(root))
                l1.addWidget(b)

            C(Item)

        l.addWidget(w1)

        w1 = QWidget()
        l1 = QHBoxLayout()
        w1.setLayout(l1)

        b = QPushButton('Refresh')
        b.clicked.connect(lambda _: self.refresh(root))
        l1.addWidget(b)

        b = QPushButton('Export')
        b.clicked.connect(lambda _: self.export(root))
        l1.addWidget(b)

        l.addWidget(w1)

        w2 = QWidget()
        l = QHBoxLayout()
        w2.setLayout(l)

        w3 = QWidget()
        l2 = QVBoxLayout()
        w3.setLayout(l2)
        l.addWidget(w3, 2)

        l2.addWidget(self.tree, 6)

        w4 = QWidget()
        self.edit_layout = QVBoxLayout()
        w4.setLayout(self.edit_layout)
        l2.addWidget(w4, 4)

        layout = QVBoxLayout()
        w3 = QWidget()
        w3.setLayout(layout)
        l.addWidget(w3, 8)

        l = QVBoxLayout()
        l.addWidget(w, 1)
        l.addWidget(w2, 30)

        layout.addWidget(QLabel('Null'))
        self.layout = layout

        container = QWidget()
        container.setLayout(l)

        self.setCentralWidget(container)

    def iter(self, item: QTreeWidgetItem):
        n = item.childCount()
        for i in range(n):
            yield item.child(i)

    def set_layout(self, lroot: QBoxLayout, root):
        for item in self.iter(root):
            name = item.text(1)
            value = json.loads(item.text(2))
            if name == "Group":
                _lroot = Group.add(lroot, value)
                self.set_layout(_lroot, item)
                continue

            K[name].add(lroot, value)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def item_selected(self):
        selected_items = self.tree.selectedItems()
        if selected_items:
            self.clear_layout(self.edit_layout)
            item = selected_items[0]
            if item.text(0) != 'Root':
                name = item.text(1)
                value = json.loads(item.text(2))

                def update(k, v):
                    value = json.loads(item.text(2))
                    value[k] = v
                    item.setText(2, json.dumps(value))

                if name == "Group":
                    Group.edit(self.edit_layout, value, update)
                else:
                    K[name].edit(self.edit_layout, value, update)

    def refresh(self, root: QTreeWidgetItem):
        self.clear_layout(self.layout)
        self.set_layout(self.layout, root)

    def export(self, root: QTreeWidgetItem):

        def A(p, t, p_s, text):
            for item in self.iter(p):
                name = item.text(1)
                value = json.loads(item.text(2))
                if name == "Group":
                    _p_s, text = Group.A(t, p_s, text, value)
                    text = A(item, t + 1, _p_s, text)
                else:
                    text = K[name].A(t, p_s, text, value)

            return text

        text = A(root, 1, 'self.layout', '\n\n------------\n\n')

        print(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
