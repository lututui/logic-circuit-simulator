from PySide6.QtCore import QTimer
from PySide6.QtGui import QBrush, QColor

from gates.gate_item import GateItem


class LEDGate(GateItem):
    def __init__(self, x, y, editor, w=80, h=50):
        super().__init__(x, y, 1, 0, editor, w, h)

    def update_graphics(self):
        match self.state:
            case None:
                self.setBrush(QBrush(QColor("lightgray")))
            case True:
                self.setBrush(QBrush(QColor("green")))
            case False:
                self.setBrush(QBrush(QColor("red")))

    def compute_output(self):
        for wire in self.connected_wires:
            if wire.dst_gate == self:
                return wire.src_gate.state
        return None
