import math

from PySide6.QtGui import QPainter, QPen, QBrush, QPainterPath, Qt
from PySide6.QtWidgets import QGraphicsTextItem

from gate_item import GateItem


class AndGate(GateItem):
    def __init__(self, x, y, editor, w=80, h=50):
        super().__init__(x, y, math.inf, math.inf, editor, w, h)

        self.label = QGraphicsTextItem('AND', parent=self)
        
    def compute_output(self):
        inputs = [t.src_gate.state for t in self.connected_inputs]

        if None in inputs or len(inputs) == 0:  # not enough info yet
            return None

        return all(inputs)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.setBrush(QBrush(Qt.GlobalColor.lightGray))

        w = self.rect().width()
        h = self.rect().height()

        # Draw AND gate shape:
        path = QPainterPath()
        path.moveTo(0, 0)          # top-left
        path.lineTo(w/2, 0)        # top mid
        path.arcTo(w/2, 0, w/2, h, 90, -180)  # semicircle on the right
        path.lineTo(0, h)          # bottom-left
        path.closeSubpath()

        painter.drawPath(path)
