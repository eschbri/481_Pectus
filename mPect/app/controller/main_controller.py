import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal
from app.Model import Model
from matplotlib import pyplot as plt
import numpy as np
from skimage import feature
import StringIO

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

        self.mode = "slice"
        self.view.plotText.setText("<p>Slice Mode</p>")

    def addLabelText(self, text):
        self.labelText = text

    def addFigure(self, name, fig):
        self.figures[name] = fig

    # Handler for viewing the body. Should be replaced with 3D image.
    def showPlot(self):
        if self.model is not None and "bodyFigure" in self.figures:
            fig = self.figures["bodyFigure"].figure

            self.constraints = []

            self.model.get2D("xy", fig, self.sliceAction)

            self.figures["bodyFigure"].draw()

    # Button handler for viewing the slice
    def viewSlice(self):
        if len(self.constraints) > 0 and "sliceFigure" in self.figures:

            # Clear the figure
            self.figures["sliceFigure"].figure.clf()

            # Get the slice
            self.slice = self.model.sliceY(self.constraints[len(self.constraints) - 1][1])

            # Set up the slice plot
            axes = self.figures["sliceFigure"].figure.add_subplot(111)
            axes.axis([0,self.model.maxx, 0, self.model.maxx])
            axes.set_axis_off()

            # Plot all the lines
            for r in self.slice.lines:
                axes.plot([r[0][0], r[1][0]], [r[0][1], r[1][1]], 'b-')

            self.figures["sliceFigure"].draw()
        else:
            print "Oh no"

    # Function that occurs on click of the left figure
    # Returns a function closure
    def sliceAction(self, axes):
        s = self
        def inSlice(event):
            # Throw the click coords into the list of lines called "constraints"
            s.constraints.append((event.xdata.item(), event.ydata.item()))

            # Plot the dotted line
            axes.plot([self.model.minx, self.model.maxx], [event.ydata.item(), event.ydata.item()], 'r--')
            self.figures["bodyFigure"].draw()
            s.viewSlice()

        return inSlice

    # Modify the slice by clipping off a portion of it
    # p1 and p2 make the line, and p3 is the direction in which to erase.
    def editSlice(self, p1, p2, p3):
        # For undo purposes
        self.oldSlice = self.slice

        self.slice.chop(p1,p2,p3)

        # TODO: ReDraw the slice image with the new slice


    # Action for clicking the slice figure
    # Has three modes: First point, second point, eraser
    def editAction(self, axes):
        s = self
        def inAction(event):
            # Make sure we're in edit mode
            if s.mode != "edit":
                return

            c = 0

            p1, p2, p3 = (0, 0)

            if c == 0:
                p1 = (event.xdata.item(), event.ydata.item())
            elif c == 1:
                p2 = (event.xdata.item(), event.ydata.item())
                #TODO: Draw a line

            elif c == 2:
                # Eraser Mode
                p3 = (event.xdata.item(), event.ydata.item())

                # Edit the slice with this data
                s.editSlice(p1, p2, p3)


            c = c + 1
            if c > 2:
                c = 0

        return inAction


    # Edit Mode Button Handler
    def editModeAction(self):
        if self.mode == "slice":
            self.switchMode("edit")
            self.view.plotText.setText("<p>Edit Mode</p>")
            self.view.eBtn.setText("Slice Mode")
        elif self.mode == "edit":
            self.switchMode("slice")
            self.view.plotText.setText("<p>Slicer Mode</p>")
            self.view.eBtn.setText("Edit Mode")


        # TODO: Add edit mode functionality

    # Save the slice image to a buffer
    def saveSlice(self):
        imgBuffer = StringIO.StringIO()
        if len(self.constraints) > 0 and "sliceFigure" in self.figures:
            #self.figures["sliceFigure"].figure.savefig('slice.png')
            self.figures["sliceFigure"].figure.savefig(imgBuffer, format='png')

        self.labelText.setText("Saved slice as `slice.png`")
        return imgBuffer

    # Flip the body on the Y axis
    def flipY(self):
        if self.model is not None:
            self.model.flip(False, True, False)
            self.showPlot()

    # Modify the mode
    def switchMode(self, mode):
        self.mode = mode
