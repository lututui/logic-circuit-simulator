from itertools import chain

from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem


class GateItem(QGraphicsRectItem):
    def __init__(self, x, y, n_inputs, n_outputs, editor, w=80, h=50):
        super().__init__(0, 0, w, h)
        self.editor = editor
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("lightgray")))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.n_inputs = n_inputs
        self.n_outputs = n_outputs

        self.input_point = None
        self.output_point = None

        self.add_input_point(h, w)
        self.add_output_point(h, w)

        # Keep track of connected wires
        self.connected_inputs = []
        self.connected_outputs = []
        self.state = None

    def add_input_point(self, h, w):
        if self.n_inputs <= 0:
            return

        # Input point (blue, left side)
        self.input_point = QGraphicsEllipseItem(-5, h / 2 - 5, 10, 10, self)
        self.input_point.setBrush(QBrush(QColor("blue")))
        self.input_point.setData(0, "input")
        self.input_point.parent_gate = self

    def add_output_point(self, h, w):
        if self.n_outputs <= 0:
            return

        # Output point (red, right side)
        self.output_point = QGraphicsEllipseItem(w - 5, h / 2 - 5, 10, 10, self)
        self.output_point.setBrush(QBrush(QColor("red")))
        self.output_point.setData(0, "output")
        self.output_point.parent_gate = self


    def update_graphics(self):
        return

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.GraphicsItemChange.ItemPositionChange:
            for wire in chain(self.connected_inputs, self.connected_outputs):
                wire.update_position()
        return super().itemChange(change, value)

    def eval(self):
        eval_result = []

        for wire in self.connected_inputs:
            eval_result.append(wire.src_gate.eval())

        return eval_result

    def remove(self):
        for wire in list(self.connected_inputs + self.connected_outputs):
            wire.remove()

        for gate in self.editor.gates:
            gate.remove()

        self.scene().removeItem(self)

    def mousePressEvent(self, event, /):
        if self.editor.current_tool == "Remove Gate":
            self.remove()

        super().mousePressEvent(event)

