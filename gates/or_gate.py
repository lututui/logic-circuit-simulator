import math

from PySide6.QtWidgets import QGraphicsTextItem

from gates.gate_item import GateItem


class OrGate(GateItem):
    def __init__(self, x, y, w=80, h=50):
        super().__init__(x, y, math.inf, math.inf, w, h)

        self.label = QGraphicsTextItem('OR', parent=self)

    def eval(self):
        return any(super().eval())

