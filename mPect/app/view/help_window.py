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
        heading = QLabel("<h1>Pectus Volume Help</h1>")
        divider = QLabel("<hr>")
        part1 = QLabel("""
            <h2>1. Loading a model</h2>
            <p>
                First, load a model using the open dialog. Choose a valid .obj file and it will 
                appear in the frame on the left side of the application.
            </p>
        """)

        part2 = QLabel("""
            <h2>2. Choosing a slice and modifying the model</h2>
            <p>
                If the model does not load in the correct orientation, use the edit menu to flip the
                slice to the desired orientation.
            <p>
            <p>
                Once the model is in the correct orientation, click the model to choose a slice. The 
                slice will then appear in the frame to the right of the application
            </p>
        """)

        part3 = QLabel("""
            <h2>3. Editing the slice</h2>
            <p>
                Once the slice is loaded in the frame to the right, click the "Edit slice" button on the
                bottom of the UI. This places the slice in Edit Mode (To switch out of edit mode, click 
                the same button, now labelled "select slice").<br>Once in Edit Mode, click somewhere on the slice 
                to begin slice modification. The first two clicks define a line, and the third click (one one 
                side of the line) removes all points to that side of the line.
            </p>
        """)

        part4 = QLabel("""
            <h2>4. Analyzing the slice</h2>
            <p>
                Once the slice is modified to the desired shape, use one of the three index generation buttons 
                as follows:
            </p>
            <h3>a. Haller Index</h3>
            <p>The Haller Index is automatic and returns an index immediately with no interaction.</p>
            <h3>b. Defect Ratio</h3>
            <p>After clicking the defect ratio, choose two points on the bottom of the slice to define the defect area. 
            The application then calculates the ratio of the area of the defect to the area of the chest slice.</p>
            <h3>c. Asymmetry Ratio</h3>
            <p>After clicking the asymmetry ratio button, select one point on the slice to define the midpoint. The 
            application then returns the ratio of the left side of the line to the right</p>
        """)

        body.addWidget(heading)
        body.addWidget(divider)
        body.addWidget(part1)
        body.addWidget(part2)
        body.addWidget(part3)
        body.addWidget(part4)
        body.addStretch(1)
