from PyQt4.QtGui import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import webbrowser

from app.view.help_window import HelpWindow


class main_window(QMainWindow):

    def __init__(self):
        super(main_window, self).__init__()

    def add_controller(self, controller):
        self.controller = controller

    def initUI(self):
        self.statusBar().showMessage('Ready')

        self.addMenuBar()

        # Create and set a central widget
        self.cwidg = QWidget(self)
        self.setCentralWidget(self.cwidg)

        self.setupLayout()

        self.resize(1600, 800)
        self.move(50,50)
        self.setWindowTitle("MPect")


    def addMenuBar(self):
        mbar = self.menuBar()

        fileMenu = mbar.addMenu('&File')
        editMenu = mbar.addMenu('&Edit')
        helpMenu = mbar.addMenu('&Help')

        self.setFileActions(fileMenu)
        self.setEditActions(editMenu)
        self.setHelpActions(helpMenu)

    def setFileActions(self, menu):

        # actions
        exitAction = QAction('&Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit')
        exitAction.triggered.connect(qApp.quit)


        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open file')
        openAction.triggered.connect(self.openDialog)

        menu.addAction(openAction)
        menu.addSeparator()
        menu.addAction(exitAction)

    def setEditActions(self, menu):
        flipXAction = QAction('&Flip X-Axis', self)
        flipXAction.setStatusTip('Flip the model along the X Axis')
        flipXAction.triggered.connect(self.controller.flipX)

        flipYAction = QAction('&Flip Y-Axis', self)
        flipYAction.setStatusTip('Flip the model along the Y Axis')
        flipYAction.triggered.connect(self.controller.flipY)

        flipZAction = QAction('&Flip Z-Axis', self)
        flipZAction.setStatusTip('Flip the model along the Z Axis')
        flipZAction.triggered.connect(self.controller.flipZ)

        menu.addAction(flipXAction)
        menu.addAction(flipYAction)
        menu.addAction(flipZAction)

    def openReadme(self):
       webbrowser.open_new("https://github.com/eschbri/481_Pectus/blob/master/README.md")

    def setHelpActions(self, menu):
        readmeAction = QAction('&Github Readme', self)
        readmeAction.setStatusTip('View the Readme on GitHub')
        readmeAction.triggered.connect(self.openReadme)

        helpAction = QAction('&Help', self)
        helpAction.setShortcut('f1')
        helpAction.setStatusTip('Open the Help Window')
        helpAction.triggered.connect(self.openHelpWindow)

        menu.addAction(helpAction)
        menu.addSeparator()
        menu.addAction(readmeAction)

    def openHelpWindow(self):
        if self.controller.helpWindow is None:
            self.controller.helpWindow = HelpWindow()
            self.controller.helpWindow.show()
        else:
            self.controller.helpWindow.show()

    def printHaller(self, ind):
        self.hallerText.setText("<b>Haller Index:</b> " + str(ind))

    def printDefect(self, ind):
        self.defectText.setText("<b>Defect Ratio:</b>: " + str(ind))

    def printAssym(self, ind):
        self.assymText.setText("<b>Assymetry Ratio:</b> " + str(ind))

    def resetAllRatios(self):
        self.printHaller("n/a")
        self.printDefect("n/a")
        self.printAssym("n/a")

    def setupLayout(self):
        plotBox = QHBoxLayout()

        rightPlotBox = QVBoxLayout()

        statsBox = QVBoxLayout()

        self.hallerText = QLabel("<b>Haller Index:</b> ")
        self.defectText = QLabel("<b>Defect Ratio:</b> ")
        self.assymText = QLabel("<b>Assymetry Ratio:</b> ")
        self.resetAllRatios()

        statsBox.addWidget(self.hallerText)
        statsBox.addWidget(self.defectText)
        statsBox.addWidget(self.assymText)

        rightPlotBox.addLayout(statsBox)
        rightPlotBox.addWidget(self.setUpPlot("sliceFigure"))

        plotBox.addWidget(self.setUpPlot("bodyFigure"))
        plotBox.addLayout(rightPlotBox)

        buttonBox = QHBoxLayout()

        self.yBtn = QPushButton('Flip Y')
        self.sBtn = QPushButton('Save Slice')
        self.eBtn = QPushButton('Edit Slice')
        self.hBtn = QPushButton('Haller Index')
        self.dBtn = QPushButton('Defect/Chest Ratio')
        self.aBtn = QPushButton('Asymmetry Ratio')

        self.yBtn.clicked.connect(self.controller.flipY)
        self.sBtn.clicked.connect(self.controller.saveSlice)
        self.eBtn.clicked.connect(self.controller.editModeAction)
        self.hBtn.clicked.connect(self.controller.hallerIndexDisplay)
        self.dBtn.clicked.connect(self.controller.defectMode)
        self.aBtn.clicked.connect(self.controller.asymmetryMode)

        buttonBox.addStretch(1)
        buttonBox.addWidget(self.yBtn)
        buttonBox.addWidget(self.eBtn)
        buttonBox.addWidget(self.sBtn)
        buttonBox.addWidget(self.hBtn)
        buttonBox.addWidget(self.dBtn)
        buttonBox.addWidget(self.aBtn)

        vbox = QVBoxLayout()

        self.plotText = QLabel()
        self.plotText.setText("<b>Open a file with Ctrl+O</b>")
        self.controller.addLabelText(self.plotText)


        vbox.addWidget(self.plotText)
        vbox.addLayout(plotBox)
        vbox.addLayout(buttonBox)

        self.cwidg.setLayout(vbox)

    def setUpPlot(self, name):
        fig = Figure(figsize=(300,300), dpi=72)
        f = FigureCanvas(fig)

        fig.patch.set_facecolor('white')

        self.controller.addFigure(name, f)

        return f

    def openDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')

        if filename:
            self.statusBar().showMessage("Opening " + filename)
            self.controller.load_model(filename)

    def reshow(self):
        self.show()

    def attachText(self, text):
        l = QLabel()
        l.setText(text)

        self.addWidget(l)
