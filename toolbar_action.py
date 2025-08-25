import qtawesome
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QToolBar


class Toolbar(QToolBar):
    def __init__(self, editor):
        super().__init__()

        self.editor = editor

        group = QActionGroup(self)
        group.setExclusive(True)

        actions = [
            QAction(qtawesome.icon('fa6s.arrow-pointer'), "Pointer", self, checkable=True, checked=True),
            QAction(qtawesome.icon('fa6s.scissors'), "Wire Cutter", self, checkable=True)
        ]

        for action in actions:
            group.addAction(action)
            self.addAction(action)

            action.triggered.connect(lambda checked, act=action.text(): self.set_tool(act))

    def set_tool(self, object_name):
        self.editor.current_tool = object_name

        print(self.editor.current_tool)
