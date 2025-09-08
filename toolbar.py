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
            QAction(qtawesome.icon('fa6s.scissors'), "Wire Cutter", self, checkable=True),
            QAction(qtawesome.icon('fa6s.trash'), "Remove Gate", self, checkable=True),
        ]

        for action in actions:
            group.addAction(action)
            self.addAction(action)

            action.triggered.connect(lambda checked, act=action.text(): self.set_tool(act))

        self.addSeparator()

        gates = [
            QAction("FALSE", self, checkable=True, whatsThis='False Emitter'),
            QAction("TRUE", self, checkable=True, whatsThis='True Emitter'),
            QAction("LED", self, checkable=True, whatsThis='LED Output'),
            QAction("OR", self, checkable=True, whatsThis='Or Gate'),
            QAction("AND", self, checkable=True, whatsThis='And Gate'),
            QAction("NOT", self, checkable=True, whatsThis='Not Gate'),
        ]

        for gate in gates:
            group.addAction(gate)
            self.addAction(gate)

            gate.triggered.connect(lambda checked, act=gate.text(): self.set_tool(f'GATE_{act}'))

    def set_tool(self, object_name):
        self.editor.current_tool = object_name
