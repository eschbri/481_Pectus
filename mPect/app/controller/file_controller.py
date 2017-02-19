import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal

class file_controller(QObject):

    def __init__(self, loader):
        super(file_controller, self).__init__()

        self.fSignal = pyqtSignal(str, name='fSignal')

        self.loader = loader

        self.fSignal.connect(self.loader)
