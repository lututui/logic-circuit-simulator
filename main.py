import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView,
    QGraphicsEllipseItem, QGraphicsLineItem, QMainWindow
)

from gates.and_gate import AndGate
from gates.false_gate import FalseGate
from gates.gate_item import GateItem
from gates.led_gate import LEDGate
from gates.or_gate import OrGate
from gates.true_gate import TrueGate
from toolbar_action import Toolbar


class WireItem(QGraphicsLineItem):
    def __init__(self, src_gate, dst_gate, editor):
        super().__init__()

        self.editor = editor

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

    def remove(self):
        self.src_gate.connected_wires.remove(self)
        self.dst_gate.connected_wires.remove(self)
        self.scene().removeItem(self)

    def mousePressEvent(self, event, /):
        if self.editor.current_tool == "Wire Cutter":
            self.remove()

        super().mousePressEvent(event)


class LogicCircuitEditor(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.simulation_timers = {}
        self.gates = [
            AndGate(50, 50, self),
            OrGate(250, 100, self),
            TrueGate(50, 100, self),
            LEDGate(250, 50, self),
            FalseGate(50, 50, self),
        ]

        for gate in self.gates:
            self.scene.addItem(gate)

        # Wiring tool state
        self.pending_endpoint = None   # (gate, point_type)
        self.temp_line = None  # temporary line while dragging
        self.current_tool = "Pointer"

    def _handle_wiring_event(self, item: QGraphicsEllipseItem):
        point_type = item.data(0)
        gate = item.parentItem()

        if isinstance(gate, GateItem):
            # Step 1: First click (either output OR input)
            if self.pending_endpoint is None:
                self.pending_endpoint = (gate, point_type)
                item.setBrush(QBrush(QColor("green")))

                if point_type == "output":
                    start = gate.output_point.sceneBoundingRect().center()
                elif point_type == "input":
                    start = gate.input_point.sceneBoundingRect().center()
                else:
                    return

                # Start temporary dashed wire
                self.temp_line = QGraphicsLineItem(start.x(), start.y(), start.x(), start.y())
                self.temp_line.setZValue(-1)  # behind all interactive items
                self.temp_line.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
                self.temp_line.setPen(QPen(Qt.GlobalColor.darkGray, 2, Qt.PenStyle.DashLine))
                self.scene.addItem(self.temp_line)
                return

            # Step 2: Second click must be the opposite type
            prev_gate, prev_type = self.pending_endpoint
            if prev_type != point_type:  # only allow input→output or output→input
                if prev_type == "output" and point_type == "input":
                    src_gate = prev_gate
                    dst_gate = gate
                elif prev_type == "input" and point_type == "output":
                    src_gate = gate
                    dst_gate = prev_gate
                else:
                    return

                wire = WireItem(src_gate, dst_gate, self)
                self.scene.addItem(wire)

        self._handle_wiring_event_cancel()

    def _handle_wiring_event_cancel(self):
        # Clicked elsewhere → cancel
        if self.pending_endpoint:
            gate, io_type = self.pending_endpoint

            if io_type == "output":
                gate.output_point.setBrush(QBrush(QColor("red")))
            elif io_type == "input":
                gate.input_point.setBrush(QBrush(QColor("blue")))

            self.pending_endpoint = None

            if self.temp_line:
                self.scene.removeItem(self.temp_line)
                self.temp_line = None


    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        item = self.itemAt(pos)

        if self.current_tool == "Pointer":
            if isinstance(item, QGraphicsEllipseItem):
                self._handle_wiring_event(item)
                return

            self._handle_wiring_event_cancel()
        elif self.current_tool.startswith("GATE_"):
            scene_pos = self.mapToScene(event.position().toPoint())

            possible_gates = {
                'GATE_FALSE': FalseGate,
                'GATE_TRUE': TrueGate,
                'GATE_LED': LEDGate,
                'GATE_AND': AndGate,
                'GATE_OR': OrGate,
            }

            gate = possible_gates.get(self.current_tool)
            new_gate = gate(scene_pos.x() - 40, scene_pos.y() - 20, self)

            self.gates.append(new_gate)
            self.scene.addItem(new_gate)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Update temporary wire while dragging"""
        if self.pending_endpoint and self.temp_line:
            gate, io_type = self.pending_endpoint

            if io_type == "output":
                start = gate.output_point.sceneBoundingRect().center()
                end = self.mapToScene(event.position().toPoint())
            else:
                start = self.mapToScene(event.position().toPoint())
                end = gate.input_point.sceneBoundingRect().center()

            self.temp_line.setLine(start.x(), start.y(), end.x(), end.y())

        super().mouseMoveEvent(event)


class LogicCircuitSimulatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logic Circuit Simulator")
        self.resize(1200, 800)

        self.editor = LogicCircuitEditor()
        self.setCentralWidget(self.editor)

        self.addToolBar(Toolbar(self.editor))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogicCircuitSimulatorWindow()

    window.show()

    sys.exit(app.exec())
