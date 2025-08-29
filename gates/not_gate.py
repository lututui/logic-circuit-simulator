import math

from PySide6.QtWidgets import QGraphicsTextItem

from gates.gate_item import GateItem


class NotGate(GateItem):
    def __init__(self, x, y, editor, w=80, h=50):
        super().__init__(x, y, math.inf, math.inf, editor, w, h)

        self.label = QGraphicsTextItem('NOT', parent=self)

    def compute_output(self):
        if len(self.connected_inputs) == 0:
            return None

        return self.connected_inputs[0].src_gate.state

