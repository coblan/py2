from PyQt4.QtGui import QWidget

class DirToolTab(QWidget):
    def __reduce__(self):
        dc={'title':self.windowTitle()}
        return self.__class__,tuple(),dc
    
    def __setstate__(self,state):
        self.setWindowTitle(state['title'])