from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gate_item import GateItem
    from editor import LogicCircuitEditor
    from PySide6.QtWidgets import QGraphicsSceneMouseEvent

from PySide6.QtGui import QPen, Qt
from PySide6.QtWidgets import QGraphicsLineItem


class WireItem(QGraphicsLineItem):
    def __init__(self, src_gate: 'GateItem', dst_gate: 'GateItem', editor: 'LogicCircuitEditor'):
        super().__init__()

        self.editor = editor

        self.src_gate = src_gate
        self.dst_gate = dst_gate
        self.setPen(QPen(Qt.GlobalColor.black, 2))

        src_gate.connected_outputs.append(self)
        dst_gate.connected_inputs.append(self)
        self.update_position()

    def update_position(self):
        p1 = self.src_gate.output_point.sceneBoundingRect().center()
        p2 = self.dst_gate.input_point.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def remove(self):
        self.src_gate.connected_outputs.remove(self)
        self.dst_gate.connected_inputs.remove(self)
        self.scene().removeItem(self)

    def mousePressEvent(self, event : 'QGraphicsSceneMouseEvent', /):
        if self.editor.current_tool == "Wire Cutter":
            self.remove()

        super().mousePressEvent(event)
