import math

from PySide6.QtWidgets import QGraphicsTextItem

from gates.gate_item import GateItem


class AndGate(GateItem):
    def __init__(self, x, y, editor, w=80, h=50):
        super().__init__(x, y, math.inf, math.inf, editor, w, h)

        self.label = QGraphicsTextItem('AND', parent=self)
        
    def compute_output(self):
        inputs = [t.src_gate.state for t in self.connected_inputs]

        if None in inputs or len(inputs) == 0:  # not enough info yet
            return None

        return all(inputs)