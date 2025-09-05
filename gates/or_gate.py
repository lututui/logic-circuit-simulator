import math

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QBrush, QPainterPath
from PySide6.QtWidgets import QGraphicsTextItem

from gate_item import GateItem


class OrGate(GateItem):
    def __init__(self, x, y, editor, w=80, h=50):
        super().__init__(x, y, math.inf, math.inf, editor, w, h)

        self.label = QGraphicsTextItem('OR', parent=self)

    def compute_output(self):
        inputs = [t.src_gate.state for t in self.connected_inputs]

        if None in inputs or len(inputs) == 0:  # not enough info yet
            return None

        return any(inputs)

    def add_input_point(self, h, w):
        super().add_input_point(h, w)

        self.input_point.setPos(25, self.input_point.pos().y())


    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # nice rounded strokes
        pen = QPen(Qt.GlobalColor.black, 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(QBrush(Qt.GlobalColor.lightGray))

        r = self.rect()
        x0, y0, w, h = r.x(), r.y(), r.width(), r.height()

        # proportion constants (tweak to taste)
        pad_left = w * 0.12     # inset of the left “start” point
        c1x  = w * 0.85     # controls the outer right bulge
        c2x  = w * 0.98
        inner_cx = w * 0.40  # controls the left concave edge

        path = QPainterPath()
        # start top-left (slightly inset)
        path.moveTo(x0 + pad_left, y0)

        # outer top curve -> nose (right point)
        path.cubicTo(x0 + c1x, y0,
                     x0 + c2x, y0 + h * 0.28,
                     x0 + w,   y0 + h * 0.5)

        # outer bottom curve -> back to bottom-left
        path.cubicTo(x0 + c2x, y0 + h * 0.72,
                     x0 + c1x, y0 + h,
                     x0 + pad_left, y0 + h)

        # inner left concave curve -> back to start
        path.cubicTo(x0 + inner_cx, y0 + h * 0.85,
                     x0 + inner_cx, y0 + h * 0.15,
                     x0 + pad_left,    y0)

        path.closeSubpath()
        painter.drawPath(path)

    # Optional: make selection/hit-test match the drawn shape
    def shape(self):
        r = self.rect()
        x0, y0, w, h = r.x(), r.y(), r.width(), r.height()
        pad_left = w * 0.12
        c1x, c2x, inner_cx = w * 0.85, w * 0.98, w * 0.40
        p = QPainterPath()
        p.moveTo(x0 + pad_left, y0)
        p.cubicTo(x0 + c1x, y0, x0 + c2x, y0 + h * 0.28, x0 + w, y0 + h * 0.5)
        p.cubicTo(x0 + c2x, y0 + h * 0.72, x0 + c1x, y0 + h, x0 + pad_left, y0 + h)
        p.cubicTo(x0 + inner_cx, y0 + h * 0.85, x0 + inner_cx, y0 + h * 0.15, x0 + pad_left, y0)
        p.closeSubpath()
        return p
