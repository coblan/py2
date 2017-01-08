from PyQt4.QtGui import QTreeView,QStandardItemModel
from heStruct.heSignal import connect,fire
class Outline(QTreeView):
    def __init__(self,p=None):
        super(Outline,self).__init__(p)
        connect('outline_set_model',self.setModel)
        self.clicked.connect(self.clicked_handel)
    
    def clicked_handel(self,index):
        item=self.model().itemFromIndex(index)
        fire('outline_click_item',self.model(),item)
        
    def __reduce__(self):
        dc={'title':self.windowTitle(),}
        return self.__class__,tuple(),dc
    def __setstate__(self,state):
        self.setWindowTitle(state.get('title'))