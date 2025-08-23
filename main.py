import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView,
    QGraphicsEllipseItem, QGraphicsLineItem
)

from gates.and_gate import AndGate
from gates.gate_item import GateItem
from gates.led_gate import LEDGate
from gates.or_gate import OrGate
from gates.true_gate import TrueGate


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
        gate1 = AndGate(50, 50)
        gate2 = OrGate(250, 100)
        gate3 = TrueGate(50, 100)
        gate4 = LEDGate(250, 50)
        self.scene.addItem(gate1)
        self.scene.addItem(gate2)
        self.scene.addItem(gate3)
        self.scene.addItem(gate4)

        # Wiring tool state
        self.pending_output = None
        self.temp_line = None  # temporary line while dragging

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        item = self.itemAt(pos)

        if isinstance(item, QGraphicsEllipseItem):
            point_type = item.data(0)
            gate = item.parentItem()

            if isinstance(gate, GateItem):
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
    editor.setWindowTitle("Logic Circuit Simulator")
    editor.resize(1200, 800)
    editor.show()
    sys.exit(app.exec())
