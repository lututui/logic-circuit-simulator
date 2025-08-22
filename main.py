import sys
from enum import Enum

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
)

class GateTypes(Enum):
    TRUE = ('TRUE', lambda : True)
    FALSE = ('FALSE', lambda : False)
    OR = ('OR', lambda elements : any(elements))
    AND = ('AND', lambda elements : all(elements))

    def __init__(self, label, operation):
        self.label = label
        self.operation = operation

class GateItem(QGraphicsRectItem):
    def __init__(self, x, y, gate_type : GateTypes, w=80, h=50):
        super().__init__(0, 0, w, h)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("lightgray")))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        # Input point (blue, left side)
        self.input_point = QGraphicsEllipseItem(-5, h / 2 - 5, 10, 10, self)
        self.input_point.setBrush(QBrush(QColor("blue")))
        self.input_point.setData(0, "input")
        self.input_point.parent_gate = self

        # Output point (red, right side)
        self.output_point = QGraphicsEllipseItem(w - 5, h / 2 - 5, 10, 10, self)
        self.output_point.setBrush(QBrush(QColor("red")))
        self.output_point.setData(0, "output")
        self.output_point.parent_gate = self

        self.gate_type = gate_type
        self.label = QGraphicsTextItem(self.gate_type.label, parent=self)

        # Keep track of connected wires
        self.connected_wires = []

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.GraphicsItemChange.ItemPositionChange:
            for wire in self.connected_wires:
                wire.update_position()
        return super().itemChange(change, value)


class WireItem(QGraphicsLineItem):
    def __init__(self, src_gate: GateItem, dst_gate: GateItem):
        super().__init__()
        self.src_gate = src_gate
        self.dst_gate = dst_gate
        self.setPen(QPen(Qt.GlobalColor.black, 2))

        src_gate.connected_wires.append(self)
        dst_gate.connected_wires.append(self)
        self.update_position()

    def update_position(self):
        p1 = self.src_gate.output_point.sceneBoundingRect().center()
        p2 = self.dst_gate.input_point.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())


class LogicCircuitEditor(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Example gates
        gate1 = GateItem(50, 50, GateTypes.AND)
        gate2 = GateItem(250, 100, GateTypes.OR)
        self.scene.addItem(gate1)
        self.scene.addItem(gate2)

        # Wiring tool state
        self.pending_output = None
        self.temp_line = None  # temporary line while dragging

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        item = self.itemAt(pos)

        if isinstance(item, QGraphicsEllipseItem):
            point_type = item.data(0)
            gate = item.parentItem()

            # Step 1: Click on output -> start wire
            if point_type == "output" and self.pending_output is None:
                self.pending_output = gate
                item.setBrush(QBrush(QColor("green")))  # highlight

                # Start a temporary line
                start = gate.output_point.sceneBoundingRect().center()
                self.temp_line = QGraphicsLineItem(start.x(), start.y(), start.x(), start.y())
                self.temp_line.setZValue(-1)  # behind all interactive items
                self.temp_line.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
                self.temp_line.setPen(QPen(Qt.GlobalColor.darkGray, 2, Qt.PenStyle.DashLine))
                self.scene.addItem(self.temp_line)
                return

            # Step 2: Click on input -> finalize wire
            if point_type == "input" and self.pending_output is not None:
                src_gate = self.pending_output
                dst_gate = gate
                wire = WireItem(src_gate, dst_gate)
                self.scene.addItem(wire)

                # Reset state
                src_gate.output_point.setBrush(QBrush(QColor("red")))
                self.pending_output = None
                if self.temp_line:
                    self.scene.removeItem(self.temp_line)
                    self.temp_line = None
                return

        # Clicked elsewhere → cancel
        if self.pending_output:
            self.pending_output.output_point.setBrush(QBrush(QColor("red")))
            self.pending_output = None
            if self.temp_line:
                self.scene.removeItem(self.temp_line)
                self.temp_line = None

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Update temporary wire while dragging"""
        if self.pending_output and self.temp_line:
            start = self.pending_output.output_point.sceneBoundingRect().center()
            end = self.mapToScene(event.position().toPoint())
            self.temp_line.setLine(start.x(), start.y(), end.x(), end.y())

        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = LogicCircuitEditor()
    editor.setWindowTitle("Logic Circuit Simulator (Drag-to-Connect Prototype)")
    editor.resize(600, 400)
    editor.show()
    sys.exit(app.exec())
