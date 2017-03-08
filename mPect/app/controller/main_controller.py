import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal
from app.Model import Model
from matplotlib import pyplot as plt
import numpy as np
from skimage import feature

class main_controller(QObject):

    def __init__(self, view):
        super(main_controller, self).__init__()

        self.open_file = ""
        self.opened = False
        self.model = None
        self.view = view
        self.figures = dict()

        # Controller modes
        self.mode = "init"


    def load_model(self, filename):
        self.model = Model.Model()
        self.model.initialize(filename)

        self.open_file = filename
        self.opened = True

        self.view.setWindowTitle("MPect - " + self.open_file)

        self.mode = "view"
        self.labelText.setText("Opened " + self.open_file)
        self.showPlot()

    def addLabelText(self, text):
        self.labelText = text

    def addFigure(self, name, fig):
        self.figures[name] = fig

    def showPlot(self):
        if self.model is not None and "bodyFigure" in self.figures:
            #self.model.get2D("xy")
            fig = self.figures["bodyFigure"].figure

            self.constraints = []

            self.model.get2D("xy", fig, self.sliceAction)

            self.figures["bodyFigure"].draw()

    def viewSlice(self):
        if len(self.constraints) > 0 and "sliceFigure" in self.figures:

            self.figures["sliceFigure"].figure.clf()
            slice = self.model.sliceY(self.constraints[len(self.constraints) - 1][1])

            axes = self.figures["sliceFigure"].figure.add_subplot(111)
            axes.axis([0,self.model.maxx, 0, self.model.maxx])

            axes.set_axis_off()

            for r in slice:
                axes.plot([r[0][0], r[1][0]], [r[0][1], r[1][1]], 'b-')

            self.figures["sliceFigure"].draw()
        else:
            print "Oh no"

    def sliceAction(self, axes):
        s = self
        def inSlice(event):
            s.constraints.append((event.xdata.item(), event.ydata.item()))

            axes.plot([self.model.minx, self.model.maxx], [event.ydata.item(), event.ydata.item()], 'r--')
            self.figures["bodyFigure"].draw()
            s.viewSlice()

        return inSlice

    def saveSlice(self):
        if len(self.constraints) > 0 and "sliceFigure" in self.figures:
            self.figures["sliceFigure"].figure.savefig('slice.png')

        self.labelText.setText("Saved slice as `slice.png`")

    def flipY(self):
        if self.model is not None:
            self.model.flip(False, True, False)
            self.showPlot()
