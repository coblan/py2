import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import sys
from PyQt4.QtGui import QApplication,QWidget
from win import Ui_Form
class Win(QWidget,Ui_Form):
    def __init__(self, parent=None, flags=0):
        super(Win,self).__init__(parent)
        self.setupUi(self)
        


if __name__=='__main__':
    app = QApplication(sys.argv)
    win= Win()
    win.show()
    sys.exit(app.exec_())