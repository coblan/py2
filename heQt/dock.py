from heQt.qteven import *
from PyQt4.QtGui import QSplitter
from PyQt4.QtCore import Qt
from drap_tree import DockTab

class Dock(QSplitter):
    """
    dock类，具有左中右三个位置，用于放置面板。注意面板必须是DockTab的子类。这些面板可以随意拖拽。
    例子:
    mainWin=QMainWindow()
    mainWin.dock=DockWidget()
    mainWin.setCentralWidget(mainWin.dock)
    
    mainWin.dock.setCentralWidget( QWidget() )  # 你自己的QWidget
    
    # 添加标签页，位置可以是左中右三种
    mainWin.panel1=DockPanel()
    mainWin.dock.addLeft( mainWin.panel1)
    mainWin.panel1.addTab(win)
    
    1. 注意 addLeft(tabWin),addMiddle(tabWin),addRight(tabWin)添加tabWin,这个tabWin必须是DockPanel的对象。
       因为其实现了拖拉等动作
    2. 只能保存那些能够pickle的窗口,所以如果想要保存panel状态，需要实现pickle功能
    
    """    
    def __init__(self, *args):
        super(Dock,self).__init__( *args)
        self.left = QSplitter(Qt.Vertical)
        self.middle = QSplitter(Qt.Vertical)
        self.right = QSplitter(Qt.Vertical)   


        self.left.added = False
        #self.addWidget(self.left)
        self.addWidget(self.middle)
        self.right.added = False
        #self.addWidget(self.right)        

        self.middle.addWidget(QLabel("middle"))
        self.middle.split = QSplitter()
        #self.middle.setStretchFactor(0, 1)
        #self.middle.setStretchFactor(1, 0)
        self.middle.split.added = False
        #self.middle.addWidget(self.middle.split)  

        #self.setStretchFactor(0, 0)
        #self.setStretchFactor(1, 1)
        #self.setStretchFactor(2, 0)        

        self.setChildrenCollapsible(False)

        self.left.openedWidth = 30
        self.right.openedWidth = 30
        self.middle.split.openedWidth = 30         

        self.left.p_spit = self
        self.right.p_spit = self
        self.middle.split.p_spit = self.middle

        #def updateStretchFactor(self):
        #if self.
        #self.setStretchFactor(0, 0)
        #self.setStretchFactor(1, 1)
        #self.setStretchFactor(2, 0)           
        def addLeft(self, tabWin):
            if not self.left.added:
                self.insertWidget(0, self.left)
                self.left.added = True

            tabWin.install(self.left, self, QTabWidget.East)
            return tabWin

        def addRight(self,  tabWin):
            if not self.right.added:
                self.addWidget( self.right)
                self.right.added = True        
            tabWin.install(self.right, self, QTabWidget.West)
            return tabWin
        def addMiddle(self, tabWin):
            if not self.middle.split.added:
                self.middle.addWidget( self.middle.split)
                self.middle.split.added = True 
                self.middle.setStretchFactor(0, 1)
                self.middle.setStretchFactor(1, 0) 

            tabWin.install(self.middle.split, self.middle, QTabWidget.North)
            return tabWin
        def setCentralWidget(self, win):
            self.middle.widget(0).setParent(None)
            self.middle.insertWidget(0, win)
            self.middle.setStretchFactor(0, 1)
            self.middle.setStretchFactor(1, 0)

        def saveDock(self):
            state = {}
            state["state"] = self.saveState()
            state["left"] = self._saveSplit(self.left)
            state["middle"] = self._saveMiddle()
            state["right"] = self._saveSplit(self.right)
            return QByteArray( pickle.dumps(state))
        def restoreDock(self, QByt):
            if not QByt:
                return
            if isinstance(QByt, QByteArray):
                QByt = QByt.data()
            state = pickle.loads(QByt)
            self._restoreSplit(state, self.addLeft, "left")
            self._restoreSplit(state, self.addRight, "right")
            self._restoreMiddle(state)

            self.restoreState(state.get("state", None))   

        def _saveSplit(self, split):
            dc = {"state" : split.saveState()}
            ls = []
            for i in range(split.count()):
                win = split.widget(i)
                ls.append(win)     
            dc["wins"] = ls
            dc["openedWidth"] = split.openedWidth
            return dc
        def _saveMiddle(self):
            dc = {"state" : self.middle.saveState()}
            dc["state1"] = self.middle.split.saveState()
            ls = []
            for i in range(self.middle.split.count()):
                win = self.middle.split.widget(i)
                ls.append(win)     
            dc["wins"] = ls 
            dc["openedWidth"] = self.middle.split.openedWidth
            return dc

        def _restoreMiddle(self, state):
            dc = state.get("middle", None)
            if dc:
                for win in dc["wins"]:
                    self.addMiddle(win)
                self.middle.split.restoreState(dc.get("state1", None))
                self.middle.restoreState(dc.get("state", None))
                self.middle.split.openedWidth = (dc.get("openedWidth", 100))
        def _restoreSplit(self, state, fun, name):
            innState = state.get(name, None)  
            if innState:
                for win in innState["wins"]:
                    fun(win)
                getattr(self, name).restoreState(innState["state"])   
                getattr(self, name).openedWidth = innState.get("openedWidth", 100)



class DockPanel(DockTab):
    """
      放在DockWidget中的标签页的容器
    开启了TabWidget的中文调整方向，自定义拖拽功能
    增加了点击标签切换开关。该功能主要在TabWidget.Bar<- customBar类中实现。
    
    """
    postion = [QTabWidget.North, QTabWidget.South, QTabWidget.East, QTabWidget.West]
    def __init__(self, *args):
        super().__init__( *args)
        #self.setTabBar(Bar(self))
        self.setMinimumWidth(20)
        self.setMinimumHeight(20)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        act = QAction("移除本面板", self)
        self.addAction(act)
        act.triggered.connect(self.uninstall)
        
        self.enableCrossDrag(customBar)
        self.enableChineseDirection(customBar)
    def uninstall(self):
        ls = []
        for win in self:
            ls.append(win)
        for win in ls:
            if hasattr(win, "uninstall"):
                win.uninstall()
        #print(self.parentWidget())
        p = self.parentWidget()
        self.setParent(None)
        if not p.count():
            p.setParent(None)
            p.added = False
            #pp = p.parentWidget()
            #if not isinstance(pp, QSplitter):
                #return
            #sizes = pp.sizes()
            #if self.tabPosition() == self.East:
                #pp.setSizes([0, sizes[0] + sizes[1], sizes[2]])
            #elif self.tabPosition() == self.West:
                #pp.setSizes([sizes[0], sizes[1] + sizes[2], 0])
            #elif self.TabPosition() == QTabWidget.North:
                #self.grandParSplitter.setSizes( [sizes[0] + sizes[1], 0 ])
                
    def install(self, splitter, outterSplit, pos):
        self.splitter = splitter
        self.tabBar().mainSplit = outterSplit
        self.tabBar().tabWidget = self
        
        self.grandParSplitter = outterSplit
        if splitter.orientation() == Qt.Vertical:
            #ls = [QTabWidget.East, QTabWidget.North, QTabWidget.West]
            #self.setTabPosition(ls[index])
            self.setTabPosition(pos)
            
        #self.tabBar().index = index
        self.tabBar().outSplit = splitter
        
        splitter.addWidget(self)
   
    # pickle 支持
    def __reduce__(self):
        self.pickleDict = {"wins": self.saveWins(), 
                           "position": self.postion.index(self.tabPosition()), 
                           "objectName": self.objectName(),}

        return super().__reduce__()
    def __setstate__(self, state):
        self.setObjectName(state["objectName"])
        wins = state.get("wins", None)
        self.setTabPosition(self.postion[ state.get("position", 0) ])
        if wins:
            self.restoreWins(wins)
        
    
class customBar(Bar):
    """增加点击激活标签，隐藏相应的面板  的功能"""
    #def __init__(self,  *args):
        #super().__init__( *args)
        #self.clickOnActive = False

    def contextMenuEvent(self, event):
        pos = event.globalPos ()
        menu = QMenu()
        win = self.tabwidget.widget( self.tabAt(event.pos () ) )
        if hasattr(win, "barActions"):
            menu.addActions(win.barActions)
        menu.addActions(self.tabwidget.actions())
        menu.exec_(pos)
    #def mouseDoubleClickEvent(self, e):
        #super().mouseDoubleClickEvent(e)
        #wid = self.mainSplit.sizes()
        ##if self.orient == 0:
        ##print(wid[self.index])
        #if wid[self.index] <= self.tabHigh:
            #wid[self.index] = self.tabwidget.parentWidget().openedWidth
        #else:
            #self.tabwidget.parentWidget().openedWidth = wid[self.index]
            ##self.tabwidget.parentWidget().openWid = self.openWid
            #wid[self.index] = self.tabHigh
        #self.mainSplit.setSizes(wid)
    
    def switchPanel(self):
        wid = self.mainSplit.sizes()
        index = self.mainSplit.indexOf(self.outSplit)
        if index == 0:
            absorb_index = 1
        elif index == 1:
            absorb_index = 0
        elif index == 2:
            absorb_index = 1
            
        if wid[index] <= self.tabHigh:
            #wid[index] = self.tabwidget.parentWidget().openedWidth
            wid[index] = self.outSplit.openedWidth
            wid[absorb_index] -= (self.outSplit.openedWidth - self.tabHigh)
        else:
            #self.tabwidget.parentWidget().openedWidth = wid[index]
            self.outSplit.openedWidth = wid[index]
            wid[absorb_index] += ( wid[index] - self.tabHigh)
            wid[index] = self.tabHigh
            
        self.mainSplit.setSizes(wid) 
    def mousePressEvent(self, event):
        pos = event.pos()
        self.shouldSwitch = False
        if self.currentIndex() == self.tabAt(pos) and event.button() == Qt.LeftButton :             
            self.shouldSwitch = True                          # self.shouldSwitch 的存在是因为切换标签是在mousePressEvent完成
        super().mousePressEvent(event)                         # "开关面板"，是在mouseReleaseEvent中完成，所以必须在mousePressEvent
        self.pressed = True                                    # 中记录下是否应该"开关面板"。
    def mouseReleaseEvent(self, event):
        if self.shouldSwitch :
            self.switchPanel()
        else:
            super().mouseReleaseEvent(event)


    #def mouseMoveEvent(self, event):
        #self.clickOnActive = False
        #super().mouseMoveEvent(event)
    
    #def switchPanel(self):
        #hight = QWidget.height(self.tabwidget)
        #split = self.mainSplit
        
        #self.tabwidget.resize(20, hight)
        


       



############################
#  测试代码
#############################
class Lab(IPickle, QLabel):
    def __init__(self, *args):
        super().__init__( *args)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(QAction("fff", self))
    def install(self, tab):
        tab.addTab(self, "haha")
    def __reduce__(self):
        self.pickleDict = {"text": self.text()}
        return super().__reduce__()
    def __setstate__(self, state):
        self.setText(state.get("text", None))
        
def test():
    tt, ok = QInputDialog.getText(None, "s", "f")
    if not ok:
        return
    tab = DockPanel ()
    
    tab.addTab(Lab("middle"), "当前目录")
    tab.addTab(Lab("middle"), "大纲")
    tab.addTab(QWidget(), "can't save ")
    getattr(win, tt)(tab)
    
if __name__ == "__main__":
    from qt_.qtEven import *
    import sys
    from qt_.widget.mainWidget import MainWidget
    app = QApplication(sys.argv)
    mainWin = MainWidget()
    mainWin.enableSaveSession()
    
    win = DockWidget()
    mainWin.setCentralWidget(win)
    mainWin.show()
    
    btn = QPushButton("cli")
    btn.clicked.connect(test)
    btn.show()
    
    #tab = DockTab()
    #tab.addTab(QWidget(), "hhh")
    #tab.addTab(QWidget(), "jjhh")
    #win.addLeft(tab)
    
    #tab2 = DockTab()
    #tab2.addTab(QWidget(), "hhh")
    #tab2.addTab(QWidget(), "jjhh")    
    
    #win.addMiddle(tab2)
    
    mainWin.registeSaveItem(win.restoreDock, win.saveDock, "dock")
    
    mainWin.restoreAll()
    sys.exit(app.exec_())