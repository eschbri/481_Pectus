import sys
from PyQt4.QtGui import QApplication, QWidget

from Model import Model
import view
from controller import main_controller

# The App's "Main" function
def start():
    app = QApplication(sys.argv)

    m = view.main_window()

    c = main_controller(m)

    m.add_controller(c)

    m.initUI()

    m.show()

    return app.exec_()
