from PySide6.QtCore import QTimer
from PySide6.QtGui import QBrush, QColor

from gates.gate_item import GateItem


class LEDGate(GateItem):
    def __init__(self, x, y, circuit, w=80, h=50):
        super().__init__(x, y, 1, 0, w, h)

        circuit.simulation_timers[self] = QTimer()
        circuit.simulation_timers[self].timeout.connect(self.update_color)
        circuit.simulation_timers[self].start(33)

        self.eval_result = None

    def update_color(self):
        new_eval = self.eval()

        if self.eval_result == new_eval:
            return

        self.eval_result = new_eval

        match self.eval_result:
            case None:
                self.setBrush(QBrush(QColor("lightgray")))
            case True:
                self.setBrush(QBrush(QColor("green")))
            case False:
                self.setBrush(QBrush(QColor("red")))

    def eval(self):
        result = super().eval()

        if len(result) == 0:
            return None
        elif len(result) == 1:
            return result[0]
        else:
            raise RuntimeError('Unsupported operation')
