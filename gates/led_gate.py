from PySide6.QtGui import QBrush, Qt

from gate_item import GateItem


class LEDGate(GateItem):
    def __init__(self, x, y, editor, w=80, h=50):
        super().__init__(x, y, 1, 0, editor, w, h)

    def update_graphics(self):
        match self.state:
            case None:
                self.setBrush(QBrush(Qt.GlobalColor.lightGray))
            case True:
                self.setBrush(QBrush(Qt.GlobalColor.green))
            case False:
                self.setBrush(QBrush(Qt.GlobalColor.red))

    def compute_output(self):
        if len(self.connected_inputs) == 0:
            return None

        return self.connected_inputs[0].src_gate.state
