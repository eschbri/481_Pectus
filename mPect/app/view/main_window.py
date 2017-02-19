from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog, QLabel, QPushButton

class main_window(QMainWindow):

    def __init__(self):
        super(main_window, self).__init__()

    def add_controller(self, controller):
        self.controller = controller

    def initUI(self):
        self.statusBar().showMessage('Ready')

        self.addMenuBar()
        self.addButtons()

        self.resize(800, 600)
        self.move(300,300)
        self.setWindowTitle("MPect")

    def addMenuBar(self):
        mbar = self.menuBar()

        fileMenu = mbar.addMenu('&File')

        self.addActions(fileMenu)

    def addActions(self, menu):

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

    def addButtons(self):
        btn = QPushButton('View Plot', self)
        yBtn = QPushButton('Flip Y', self)

        btn.clicked.connect(self.controller.showPlot)
        yBtn.clicked.connect(self.controller.flipY)

        btn.move(25,50)
        yBtn.move(25,100)

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
