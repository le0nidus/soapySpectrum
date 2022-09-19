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
        self.center()
        self.show()
        mainFunc.mainGUI(self)

        self.canvas = FigureCanvasQTAgg(plt.Figure(figsize=(5, 4),dpi=100))
        self.ui.frmPlot.addWidget(self.canvas)
        self.insert_ax()


    def closeEvent(self, event):
        dlg = ExitMessageBox()
        dlg.setWindowTitle("Exit dialog")
        dlg.setText("Are you sure you want to quit?<br>")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        appIcon = QIcon("icon.png")
        dlg.setWindowIcon(appIcon)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            self.running = False
            # @@@@@@@@@@@@@@@@@@@@@@ RELEASE SDR CODE @@@@@@@@@@@@@@@@@@@@@@
            # @@@@@@@@@@@@@@@@@@@@@@                  @@@@@@@@@@@@@@@@@@@@@@
            # @@@@@@@@@@@@@@@@@@@@@@                  @@@@@@@@@@@@@@@@@@@@@@
            # @@@@@@@@@@@@@@@@@@@@@@                  @@@@@@@@@@@@@@@@@@@@@@
            # @@@@@@@@@@@@@@@@@@@@@@                  @@@@@@@@@@@@@@@@@@@@@@
            # @@@@@@@@@@@@@@@@@@@@@@ RELEASE SDR CODE @@@@@@@@@@@@@@@@@@@@@@
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def insert_ax(self):
        font = {
            'weight': 'normal',
            'size': 14
        }
        rc('font', **font)
        self.ax = self.canvas.figure.subplots()

class ExitMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = self.layout()
        qt_msgbox_label = self.findChild(QLabel, "qt_msgbox_label")
        qt_msgbox_label.setAlignment(Qt.AlignCenter)
        qt_msgbox_buttonbox = self.findChild(QDialogButtonBox, "qt_msgbox_buttonbox")
        grid_layout.addWidget(qt_msgbox_label, 0, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(qt_msgbox_buttonbox, 1, 0, alignment=Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())