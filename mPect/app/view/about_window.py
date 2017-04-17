from PyQt4.QtGui import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

class AboutWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 100, 800, 600)

        self.setWindowTitle("About Pectus Volume")

        self.setupLayout()

    def setupLayout(self):
        self.body = QVBoxLayout()

        self.setLayout(self.body)

        self.writeText(self.body)

    def writeText(self, body):
        text = QLabel("""
            <h1>Pectus Volume</h1>
            <p>Written by</p>
            <ul>
                <li>Yunke Cao (ykcao@umich.edu)</li>
                <li>Brian Esch (eschbri@umich.edu)</li>
                <li>James Le (jameshle@umich.edu)</li>
                <li>Matt Solarz (mssolarz@umich.edu</li>
            </ul>
            <p>for EECS 481: Software Engineering</p>
            <p>Developed for the Michigan Pediatric Device Consortium</p>
        """)

        body.addWidget(text)
        body.addStretch(1)