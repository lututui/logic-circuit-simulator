from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem

from gate_item import GateItem
from gates.and_gate import AndGate
from gates.false_gate import FalseGate
from gates.led_gate import LEDGate
from gates.not_gate import NotGate
from gates.or_gate import OrGate
from gates.true_gate import TrueGate
from wire_item import WireItem


class LogicCircuitEditor(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

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
        self.pending_endpoint = None  # (gate, point_type)
        self.temp_line = None  # temporary line while dragging
        self.current_tool = "Pointer"

        self.sim_timer = QTimer()
        self.sim_timer.timeout.connect(self.simulation_step)
        self.sim_timer.start(50)

    def simulation_step(self):
        changed = False
        for gate in self.gates:
            new_state = gate.compute_output()  # pure function
            if new_state != gate.state:
                gate.state = new_state
                gate.update_graphics()
                changed = True
        # Optionally: loop until stable (important for feedback)
        if changed:
            self.simulation_step()

    def _handle_wiring_event(self, item: QGraphicsEllipseItem):
        point_type = item.data(0)
        gate = item.parentItem()

        if isinstance(gate, GateItem):
            # Step 1: First click (either output OR input)
            if self.pending_endpoint is None:
                self.pending_endpoint = (gate, point_type)
                item.setBrush(Qt.GlobalColor.green)

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
                    src_gate, dst_gate = prev_gate, gate
                elif prev_type == "input" and point_type == "output":
                    src_gate, dst_gate = gate, prev_gate
                else:
                    return

                if len(src_gate.connected_outputs) >= src_gate.n_outputs:
                    self._handle_wiring_event_cancel()
                    return

                if len(dst_gate.connected_inputs) >= dst_gate.n_inputs:
                    self._handle_wiring_event_cancel()
                    return

                wire = WireItem(src_gate, dst_gate, self)
                self.scene.addItem(wire)

        self._handle_wiring_event_cancel()

    def _handle_wiring_event_cancel(self):
        # Clicked elsewhere → cancel
        if self.pending_endpoint:
            gate, io_type = self.pending_endpoint

            if io_type == "output":
                gate.output_point.setBrush(Qt.GlobalColor.red)
            elif io_type == "input":
                gate.input_point.setBrush(Qt.GlobalColor.blue)

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
                'GATE_NOT': NotGate,
            }

            gate = possible_gates.get(self.current_tool)
            new_gate = gate(int(scene_pos.x() - 40), int(scene_pos.y() - 20), self)

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

    def serialize(self):
        gates_data = []
        wires_data = []

        for i, gate in enumerate(self.gates):
            gates_data.append({
                "id": i,
                "type": gate.__class__.__name__,
                "x": gate.pos().x(),
                "y": gate.pos().y()
            })

        # Give each gate a unique id
        gate_to_id = {gate: i for i, gate in enumerate(self.gates)}

        for gate in self.gates:
            for wire in gate.connected_outputs:
                wires_data.append({
                    "src": gate_to_id[wire.src_gate],
                    "dst": gate_to_id[wire.dst_gate]
                })

        return {
            "gates": gates_data,
            "wires": wires_data
        }

    def deserialize(self, data):
        # Clear existing scene
        self.scene.clear()
        self.gates.clear()

        gate_map = {}

        # Rebuild gates
        for g in data.get("gates", []):
            gate_type = g["type"]
            x, y = g["x"], g["y"]

            gate_cls = GateItem.registry.get(gate_type)

            if not gate_cls:
                raise RuntimeError(f'Unknown gate: {gate_type}')

            gate = gate_cls(x, y, self)

            self.gates.append(gate)
            self.scene.addItem(gate)
            gate_map[g["id"]] = gate

        # Rebuild wires
        for w in data.get("wires", []):
            src = gate_map.get(w["src"])
            dst = gate_map.get(w["dst"])
            if src and dst:
                wire = WireItem(src, dst, self)
                self.scene.addItem(wire)