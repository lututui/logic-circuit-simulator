import math

from PySide6.QtWidgets import QGraphicsTextItem

from gates.gate_item import GateItem


class AndGate(GateItem):
    def __init__(self, x, y, editor, w=80, h=50):
        super().__init__(x, y, math.inf, math.inf, editor, w, h)

        self.label = QGraphicsTextItem('AND', parent=self)
        
    def compute_output(self):
        inputs = []
        for wire in self.connected_wires:
            if wire.dst_gate == self:  # incoming wire
                inputs.append(wire.src_gate.state)
        if None in inputs:  # not enough info yet
            return None
        return all(inputs)