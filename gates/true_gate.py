import math

from PySide6.QtWidgets import QGraphicsTextItem

from gates.gate_item import GateItem


class TrueGate(GateItem):
    def __init__(self, x, y, editor, w=80, h=50):
        super().__init__(x, y, 0, math.inf, editor, w, h)


        self.label = QGraphicsTextItem('TRUE', parent=self)

    def eval(self):
        return True