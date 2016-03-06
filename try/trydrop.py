import sys
from PyQt4.QtGui import QApplication,QWidget,QTreeView,QTabWidget,QListView,QAbstractItemView

class Win(QListView):
    def __init__(self,p=None):
        super(Win,self).__init__(p)

        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
    def dragEnterEvent(self,event):
        event.acceptProposedAction()
    
    def dropEvent(self,Event):
        print('here')


if __name__=='__main__':
    app=QApplication(sys.argv)
    win=Win()
    win.show()
    sys.exit(app.exec_())