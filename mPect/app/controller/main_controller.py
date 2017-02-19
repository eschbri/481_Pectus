import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal
from app.Model import Model
from matplotlib import pyplot as plt

class main_controller(QObject):

    def __init__(self, view):
        super(main_controller, self).__init__()

        self.open_file = ""
        self.opened = False
        self.model = None
        self.view = view

    def load_model(self, filename):
        self.model = Model.Model()
        self.model.initialize(filename)

        self.open_file = filename
        self.opened = True

        self.view.setWindowTitle("MPect - " + self.open_file)

    def showPlot(self):
        if self.model is not None:
            self.model.get2D("xy")

    def flipY(self):
        if self.model is not None:
            self.model.flip(False, True, False)
