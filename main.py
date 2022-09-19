import sys
from PySide2 import QtCore
from PySide2.QtCore import QEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib import rc

from UI.ui_Main import *
import mainFunc
# import ctypes
#
# myappid = 'mycompany.myproduct.subproduct.version'
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon("UI/icon.png"))
        self.setMinimumSize(800, 550)
        self.running = True
        self.ui = Ui_SoapySpectrum()
        self.ui.setupUi(self)
        self.show()
        mainFunc.mainGUI(self)

        self.canvas = FigureCanvasQTAgg(plt.Figure(figsize=(5, 4),dpi=100))
        self.ui.frmPlot.addWidget(self.canvas)
        self.insert_ax()


    def closeEvent(self, event):
        self.running = False

        
    def insert_ax(self):
        font = {
            'weight': 'normal',
            'size': 14
        }
        rc('font', **font)
        self.ax = self.canvas.figure.subplots()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())