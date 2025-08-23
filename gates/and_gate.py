import math

from PySide6.QtWidgets import QGraphicsTextItem

from gates.gate_item import GateItem


class AndGate(GateItem):
    def __init__(self, x, y, w=80, h=50):
        super().__init__(x, y, math.inf, math.inf, w, h)

        self.label = QGraphicsTextItem('AND', parent=self)
        
    def eval(self):
        eval_result = super().eval()

        if len(eval_result) == 0:
            return None

        return all(super().eval())