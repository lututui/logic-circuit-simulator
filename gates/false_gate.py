import math

from PySide6.QtWidgets import QGraphicsTextItem

from gates.gate_item import GateItem


class FalseGate(GateItem):
    def __init__(self, x, y, w=80, h=50):
        super().__init__(x, y, 0, math.inf, w, h)

        self.label = QGraphicsTextItem('FALSE', parent=self)

    def eval(self):
        return False