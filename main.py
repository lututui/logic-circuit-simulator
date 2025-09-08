import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow
)

from editor import LogicCircuitEditor
from toolbar import Toolbar


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
