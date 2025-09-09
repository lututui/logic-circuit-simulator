import json
import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox
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
        self._create_menu()

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        export_action = file_menu.addAction("Save As")
        export_action.triggered.connect(self.export_to_json)

        import_action = file_menu.addAction("Open")
        import_action.triggered.connect(self.import_from_json)

    def export_to_json(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Circuit as JSON",
            "",
            "JSON Files (*.json)"
        )
        if not path:
            return

        try:
            data = self.editor.serialize()
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

    def import_from_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Circuit JSON",
            "",
            "JSON Files (*.json)"
        )
        if not path:
            return

        try:
            with open(path, "r") as f:
                data = json.load(f)
            self.editor.deserialize(data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogicCircuitSimulatorWindow()

    window.show()

    sys.exit(app.exec())
