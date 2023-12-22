from __future__ import annotations

import typing as t

import pyqtgraph as pg
from pyqtgraph.dockarea import Dock, DockArea
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

if t.TYPE_CHECKING:
    from .TopasModel import Topas


class TopasApp(QApplication):
    def __init__(self, topas=None, spectrometer=None):
        self.topas = topas
        self.spectrometer = spectrometer

        super().__init__([])


class TopasInfoLabel(QLabel):
    def __init__(self, topas):
        super().__init__()
        self.topas: Topas = topas

    def update_text(self):
        s = ""
        for name, motor in self.topas.motors.items():
            s += f"{name}: {motor.actual_position} {motor.target_position}\n"
        self.setText(s)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TopasGUI")
        self.dock_area = DockArea()
        self.specrum_plot = pg.PlotWidget()
        self.specrum_dock = Dock(
            "Spectrum", size=(400, 400), widget=self.specrum_plot, closable=False
        )
        self.dock_area.addDock(self.specrum_dock, "left")
        self.topas_dock = Dock("Topas", size=(400, 400))
        self.dock_area.addDock(self.topas_dock)

        self.setCentralWidget(self.dock_area)


if __name__ == "__main__":
    app = TopasApp([])
    mw = MainWindow()
    mw.show()
    app.exec()
