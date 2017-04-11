from PyQt4.QtGui import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout



class HelpWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 100, 800, 600)

        self.setWindowTitle("Pectus Volume Help")

        self.setupLayout()

    def setupLayout(self):
        self.body = QVBoxLayout()

        self.setLayout(self.body)

        self.writeHelp(self.body)

    def writeHelp(self, body):
        heading = QLabel("<h1>Help</h1>")
        divider = QLabel("<hr>")

        body.addWidget(heading)
        body.addWidget(divider)
        body.addStretch(1)
