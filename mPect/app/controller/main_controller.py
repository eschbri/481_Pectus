import sys
from PyQt4.QtGui import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog
from PyQt4.QtCore import QObject
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
        self.hallerAxes = None

        # Controller modes
        self.mode = "init"

        # Slice Editing Data
        self.sdata = {}

        # Area Select Data
        self.adata = {}

        # Other windows
        self.helpWindow = None


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

        self.view.resetAllRatios()

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

            self.hallerAxes = axes

            # Plot all the lines
            for r in self.slice.getLines():
                axes.plot([r[0][0], r[1][0]], [r[0][1], r[1][1]], 'b-')

            if hasattr(self, 'sliceEventID'):
                self.figures["sliceFigure"].figure.canvas.mpl_disconnect(self.sliceEventID)

            self.sliceEventID = self.figures["sliceFigure"].figure.canvas.mpl_connect('button_press_event', self.editAction(axes))
            self.sdata["c"] = 0
            self.sdata["p1"] = (0,0)
            self.sdata["p2"] = (0,0)
            self.sdata["p3"] = (0,0)
            self.adata["c"] = 0
            self.adata["p1"] = (0,0)
            self.adata["p2"] = (0,0)

            self.figures["sliceFigure"].draw()
        else:
            print "Oh no"

    # Function that occurs on click of the left figure
    # Returns a function closure
    def sliceAction(self, axes):
        s = self
        def inSlice(event):
            # Make sure we're in slice mode
            if s.mode != "slice":
                return

            # Throw the click coords into the list of lines called "constraints"
            try:
                s.constraints.append((event.xdata.item(), event.ydata.item()))

                # Plot the dotted line
                axes.plot([self.model.minx, self.model.maxx], [event.ydata.item(), event.ydata.item()], 'r--')
                self.figures["bodyFigure"].draw()
                s.viewSlice()

                self.view.resetAllRatios()
            except:
                return

        return inSlice

    # Modify the slice by clipping off a portion of it
    # p1 and p2 make the line, and p3 is the direction in which to erase.
    def editSlice(self, p1, p2, p3, axes):
        # For undo purposes
        self.oldSlice = self.slice

        self.slice.chop(p1,p2,p3)

        # TODO: ReDraw the slice image with the new slice
        axes.cla()

        axes.axis([0,self.model.maxx, 0, self.model.maxx])
        axes.set_axis_off()

        for r in self.slice.getLines():
            axes.plot([r[0][0], r[1][0]], [r[0][1], r[1][1]], 'b-')

        self.figures["sliceFigure"].draw()

    # Action for clicking the slice figure
    # Has three modes: First point, second point, eraser
    def editAction(self, axes):
        s = self
        def inAction(event):
            # Make sure we're in edit mode
            xc = 0
            yc = 0

            try:
                xc = event.xdata.item()
                yc = event.ydata.item()
            except:
                return

            if s.mode == "edit":
                if s.sdata["c"] == 0:
                    s.sdata["p1"] = (xc, yc)

                    s.view.statusBar().showMessage("P1 Selected")
                elif s.sdata["c"] == 1:
                    s.sdata["p2"] = (xc, yc)
                    #TODO: Draw a line
                    axes.plot([s.sdata["p1"][0], s.sdata["p2"][0]],[s.sdata["p1"][1], s.sdata["p2"][1]], 'r--')
                    s.figures["sliceFigure"].draw()

                    s.view.statusBar().showMessage("P2 Selected")
                elif s.sdata["c"] == 2:
                    # Eraser Mode
                    s.sdata["p3"] = (xc, yc)

                    # Edit the slice with this data
                    s.editSlice(s.sdata["p1"], s.sdata["p2"], s.sdata["p3"], axes)

                    s.view.statusBar().showMessage("P3 Selected")


                s.sdata["c"] = s.sdata["c"] + 1
                if s.sdata["c"] > 2:
                    s.sdata["c"] = 0

            elif s.mode == "defect":
                if s.adata["c"] == 0:
                    s.adata["p1"] = (event.xdata.item(), event.ydata.item())
                    axes.plot(s.adata["p1"][0], s.adata["p1"][1], 'ro')
                    s.figures["sliceFigure"].draw()
                    s.view.statusBar().showMessage("P1 Selected")
                elif s.adata["c"] == 1:
                    s.adata["p2"] = (event.xdata.item(), event.ydata.item())
                    axes.plot([s.adata["p1"][0], s.adata["p2"][0]],[s.adata["p1"][1], s.adata["p2"][1]], 'r--')
                    axes.plot(s.adata["p2"][0], s.adata["p2"][1], 'ro')
                    result = s.slice.defectRatio(s.adata["p1"][0], s.adata["p1"][1], s.adata["p2"][0], s.adata["p2"][1])
                    if result <= 0:
                        s.view.statusBar().showMessage("Select the area again")
                    else:
                        s.view.statusBar().showMessage(str(result))
                        s.view.printDefect(result)
                    s.figures["sliceFigure"].draw()
                    
                s.adata["c"] = s.adata["c"] + 1
                if s.adata["c"] > 1:
                    s.hallerAxes.cla()
                    s.hallerAxes.axis([0,s.model.maxx, 0, s.model.maxx])
                    s.hallerAxes.set_axis_off()
                    for r in s.slice.getLines():
                        s.hallerAxes.plot([r[0][0], r[1][0]], [r[0][1], r[1][1]], 'b-')
                    s.adata["c"] = 0

            elif s.mode == "asymmetry":
                x = event.xdata.item()
                midLine, = axes.plot([x, x], [0, s.model.maxy], 'r--')
                result = s.slice.asymmetryRatio(x)
                s.view.statusBar().showMessage(str(result))
                s.view.printAssym(result)
                s.figures["sliceFigure"].draw()
                axes.lines.remove(midLine)


        return inAction


    # Edit Mode Button Handler
    def editModeAction(self):
        if self.mode != "edit":
            if self.mode == "asymmetry":
                self.view.aBtn.setStyleSheet('color:#000000')
                self.reprint()
            elif self.mode == "defect":
                self.view.dBtn.setStyleSheet('color:#000000')
                self.reprint()
            elif self.mode == "haller":
                self.view.hBtn.setStyleSheet('color:#000000')
                self.reprint()
            self.switchMode("edit")
            self.view.plotText.setText("<p>Edit Mode</p>")
            self.view.eBtn.setText("Slice Mode")
        elif self.mode != "slice":
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

    def flipX(self):
        if self.model is not None:
            self.model.flip(True, False, False)
            self.showPlot()

    def flipZ(self):
        if self.model is not None:
            self.model.flip(False, False, True)
            self.showPlot()

    # Modify the mode
    def switchMode(self, mode):
        self.mode = mode

    #haller index show lines
    def hallerIndexDisplay(self):
        if self.hallerAxes != None:
            if self.mode != "haller":
                if self.mode == "asymmetry":
                    self.view.aBtn.setStyleSheet('color:#000000')
                    self.reprint()
                elif self.mode == "defect":
                    self.view.dBtn.setStyleSheet('color:#000000')
                    self.reprint()
                self.switchMode("haller")
                self.view.hBtn.setStyleSheet('color:#ff0000')

                # For undo purposes
                self.oldSlice = self.slice

                hallerPoints = self.slice.hallerIndex()

                # TODO: ReDraw the slice image with the new slice
                self.hallerAxes.cla()

                self.hallerAxes.axis([0,self.model.maxx, 0, self.model.maxx])
                self.hallerAxes.set_axis_off()

                for r in self.slice.getLines():
                    self.hallerAxes.plot([r[0][0], r[1][0]], [r[0][1], r[1][1]], 'b-')

                self.hallerAxes.plot([hallerPoints[1][0], hallerPoints[2][0]], [hallerPoints[1][1], hallerPoints[2][1]], 'r--')
                #self.hallerAxes.plot([hallerPoints[3][0], hallerPoints[4][0]], [hallerPoints[3][1], hallerPoints[4][1]], 'r--')

                #display straight horizontal line below slice 
                if hallerPoints[0] > 1.5:
                    self.hallerAxes.plot([hallerPoints[3][0], hallerPoints[4][0]], [hallerPoints[5][1] - .01, hallerPoints[5][1] - .01], 'r--')
                else: 
                    self.hallerAxes.plot([hallerPoints[3][0], hallerPoints[4][0]], [hallerPoints[3][1], hallerPoints[4][1]], 'r--')
                #print "Haller Index: " + str(hallerPoints[0]) + "vertebre point: " + str(hallerPoints[1]) + "sternum point: " + str(hallerPoints[2])
                #print "right lung point: " + str(hallerPoints[3]) + "left lung point: " + str(hallerPoints[4])

                #self.labelText.setText("haller index is: " + str(hallerPoints[0]))
                self.view.statusBar().showMessage("haller index is: " + str(hallerPoints[0]))
                self.view.printHaller(hallerPoints[0])
                self.figures["sliceFigure"].draw()
            else:
                self.switchMode("edit")
                self.view.plotText.setText("<p>Edit Mode</p>")
                self.view.eBtn.setText("Slice Mode")
                self.view.hBtn.setStyleSheet('color:#000000')
                self.reprint()

    # Button entering the defect area mode
    def defectMode(self):
        if self.mode != "defect":
            if self.mode == "asymmetry":
                self.view.aBtn.setStyleSheet('color:#000000')
                self.reprint()
            elif self.mode == "haller":
                self.view.hBtn.setStyleSheet('color:#000000')
                self.reprint()
            self.switchMode("defect")
            self.view.plotText.setText("<p>Select Defect Area</p>")
            self.view.dBtn.setStyleSheet('color:#ff0000')
        else:
            self.switchMode("edit")
            self.view.plotText.setText("<p>Edit Mode</p>")
            self.view.eBtn.setText("Slice Mode")
            self.view.dBtn.setStyleSheet('color:#000000')
            self.reprint()

    def asymmetryMode(self):
        if self.mode != "asymmetry":
            if self.mode == "defect":
                self.view.dBtn.setStyleSheet('color:#000000')
                self.reprint()
            elif self.mode == "haller":
                self.view.hBtn.setStyleSheet('color:#000000')
                self.reprint()
            self.switchMode("asymmetry")
            self.view.plotText.setText("<p>Select Middle Line</p>")
            self.view.aBtn.setStyleSheet('color:#ff0000') 

        else:
            self.switchMode("edit")
            self.view.plotText.setText("<p>Edit Mode</p>")
            self.view.eBtn.setText("Slice Mode")
            self.view.aBtn.setStyleSheet('color:#000000')
            self.reprint()

    def reprint(self):
        self.adata["c"] = 0
        self.sdata["c"] = 0
        self.hallerAxes.cla()

        self.hallerAxes.axis([0,self.model.maxx, 0, self.model.maxx])
        self.hallerAxes.set_axis_off()
        for r in self.slice.getLines():
            self.hallerAxes.plot([r[0][0], r[1][0]], [r[0][1], r[1][1]], 'b-')
        self.figures["sliceFigure"].draw()
        

