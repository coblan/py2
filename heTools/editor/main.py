from heQt.qteven import *
import sys
from PyQt4.QtGui import QApplication
from heQt.code_editor import Bridge

if __name__=='__main__':
    app=QApplication(sys.argv)
    win=Bridge()
    win.show()
    sys.exit(app.exec_())