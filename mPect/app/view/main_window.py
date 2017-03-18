from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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
        self.move(300,300)
        self.setWindowTitle("MPect")



    def addMenuBar(self):
        mbar = self.menuBar()

        fileMenu = mbar.addMenu('&File')

        self.setActions(fileMenu)

    def setActions(self, menu):

        # actions
        exitAction = QAction('&Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit')
        exitAction.triggered.connect(qApp.quit)


        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open file')
        openAction.triggered.connect(self.openDialog)

        menu.addAction(exitAction)
        menu.addAction(openAction)

    def setupLayout(self):
        plotBox = QHBoxLayout()

        plotBox.addWidget(self.setUpPlot("bodyFigure"))
        plotBox.addWidget(self.setUpPlot("sliceFigure"))

        buttonBox = QHBoxLayout()

        self.yBtn = QPushButton('Flip Y')
        self.sBtn = QPushButton('Save Slice')
        self.eBtn = QPushButton('Edit Slice')
        self.hBtn = QPushButton('Haller Index')

        self.yBtn.clicked.connect(self.controller.flipY)
        self.sBtn.clicked.connect(self.controller.saveSlice)
        self.eBtn.clicked.connect(self.controller.editModeAction)
        self.hBtn.clicked.connect(self.controller.hallerIndexDisplay)

        buttonBox.addStretch(1)
        buttonBox.addWidget(self.yBtn)
        buttonBox.addWidget(self.eBtn)
        buttonBox.addWidget(self.sBtn)
        buttonBox.addWidget(self.hBtn)

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

        self.controller.addFigure(name, f)

        return f

    def openDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')

        if filename[0]:
            self.statusBar().showMessage("Opening " + filename[0])
            self.controller.load_model(filename[0])

    def reshow(self):
        self.show()

    def attachText(self, text):
        l = QLabel()
        l.setText(text)

        self.addWidget(l)
