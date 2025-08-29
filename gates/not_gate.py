import math

from PySide6.QtGui import QBrush, QColor, QPainterPath, QPainter, QPen
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

    def paint(self, painter: QPainter, option, widget=None):
        painter.setPen(QPen(QColor("black"), 2))
        painter.setBrush(QBrush(QColor("lightgray")))

        w = self.rect().width()
        h = self.rect().height()

        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(w - 10, h / 2)  # triangle tip (before bubble)
        path.lineTo(0, h)
        path.closeSubpath()

        painter.drawPath(path)

        # Draw inversion bubble
        bubble_radius = 10
        center_x = w - 10 + bubble_radius
        center_y = h / 2
        painter.drawEllipse(center_x - bubble_radius, center_y - bubble_radius,
                            bubble_radius * 2, bubble_radius * 2)

